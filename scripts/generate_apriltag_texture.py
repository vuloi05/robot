#!/usr/bin/env python3
"""Sinh texture AprilTag chuẩn tag36h11 (ID 0) bằng libapriltag.so của ROS 2 Jazzy
và tự kiểm chứng bằng chính apriltag_detector_detect trước khi lưu file PNG.
"""

from __future__ import annotations

import ctypes
from pathlib import Path
from PIL import Image


class ImageU8(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int32),
        ("height", ctypes.c_int32),
        ("stride", ctypes.c_int32),
        ("buf", ctypes.POINTER(ctypes.c_uint8)),
    ]


class ZArray(ctypes.Structure):
    _fields_ = [
        ("el_sz", ctypes.c_size_t),
        ("size", ctypes.c_int),
        ("alloc", ctypes.c_int),
        ("data", ctypes.c_void_p),
    ]


class AprilTagDetection(ctypes.Structure):
    _fields_ = [
        ("family", ctypes.c_void_p),
        ("id", ctypes.c_int),
        ("hamming", ctypes.c_int),
        ("decision_margin", ctypes.c_float),
        ("H", ctypes.c_void_p),
        ("c", ctypes.c_double * 2),
        ("p", (ctypes.c_double * 2) * 4),
    ]


def find_libapriltag() -> ctypes.CDLL:
    candidates = [
        "/opt/ros/jazzy/lib/x86_64-linux-gnu/libapriltag.so",
        "/opt/ros/jazzy/lib/aarch64-linux-gnu/libapriltag.so",
        "libapriltag.so",
    ]
    for cand in candidates:
        p = Path(cand)
        if cand == "libapriltag.so" or p.exists():
            return ctypes.CDLL(cand)
    raise FileNotFoundError("Không tìm thấy libapriltag.so")


def main() -> None:
    lib = find_libapriltag()

    lib.tag36h11_create.restype = ctypes.c_void_p
    lib.tag36h11_destroy.argtypes = [ctypes.c_void_p]
    lib.apriltag_to_image.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    lib.apriltag_to_image.restype = ctypes.POINTER(ImageU8)
    lib.image_u8_destroy.argtypes = [ctypes.POINTER(ImageU8)]

    lib.apriltag_detector_create.restype = ctypes.c_void_p
    lib.apriltag_detector_destroy.argtypes = [ctypes.c_void_p]
    lib.apriltag_detector_add_family_bits.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_int,
    ]
    lib.apriltag_detector_detect.argtypes = [ctypes.c_void_p, ctypes.POINTER(ImageU8)]
    lib.apriltag_detector_detect.restype = ctypes.POINTER(ZArray)
    lib.apriltag_detections_destroy.argtypes = [ctypes.POINTER(ZArray)]

    tf = lib.tag36h11_create()
    if not tf:
        raise RuntimeError("tag36h11_create thất bại")

    tag_id = 0
    im_ptr = lib.apriltag_to_image(tf, tag_id)
    im = im_ptr.contents
    orig_w, orig_h, stride = im.width, im.height, im.stride

    raw = bytearray(orig_w * orig_h)
    for y in range(orig_h):
        row_off = y * stride
        for x in range(orig_w):
            raw[y * orig_w + x] = im.buf[row_off + x]

    base_img = Image.frombytes("L", (orig_w, orig_h), bytes(raw))
    lib.image_u8_destroy(im_ptr)

    # Scale nearest-neighbor sắc nét lên bội nguyên của kích thước gốc + quiet border trắng
    cell_px = 48
    scaled_w = orig_w * cell_px
    scaled_h = orig_h * cell_px
    scaled = base_img.resize((scaled_w, scaled_h), Image.Resampling.NEAREST)

    border = cell_px
    canvas_w = scaled_w + 2 * border
    canvas_h = scaled_h + 2 * border
    canvas = Image.new("L", (canvas_w, canvas_h), color=255)
    canvas.paste(scaled, (border, border))

    # Tự kiểm chứng nhận diện ngược lại bằng chính libapriltag
    td = lib.apriltag_detector_create()
    lib.apriltag_detector_add_family_bits(td, tf, 2)

    pixels = canvas.tobytes()
    buf_type = ctypes.c_uint8 * len(pixels)
    buf = buf_type.from_buffer_copy(pixels)
    test_u8 = ImageU8(canvas_w, canvas_h, canvas_w, buf)

    detections = lib.apriltag_detector_detect(td, ctypes.byref(test_u8))
    det_arr = detections.contents
    assert det_arr.size == 1, f"Kỳ vọng phát hiện 1 tag, nhận được {det_arr.size}"
    det_ptrs = ctypes.cast(det_arr.data, ctypes.POINTER(ctypes.POINTER(AprilTagDetection)))
    detected_id = det_ptrs[0].contents.id
    assert detected_id == tag_id, f"Tag ID sai: {detected_id} != {tag_id}"

    lib.apriltag_detections_destroy(detections)
    lib.apriltag_detector_destroy(td)
    lib.tag36h11_destroy(tf)

    repo_root = Path(__file__).resolve().parent.parent
    out_path = (
        repo_root
        / "ros2_ws"
        / "src"
        / "restaurant_robot_sim"
        / "models"
        / "apriltag_dock"
        / "materials"
        / "textures"
        / "tag36h11_0.png"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out_path, format="PNG")
    print(
        f"[PASS] Generated {out_path} ({canvas_w}x{canvas_h} px, raw tag {orig_w}x{orig_h}) "
        f"and verified libapriltag detection ID={detected_id}"
    )


if __name__ == "__main__":
    main()
