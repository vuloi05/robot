#!/usr/bin/env python3
"""Sinh hai mặt nạ Nav2 Costmap Filter (keepout_mask & speed_mask)
đồng kích thước, đồng origin và resolution với maps/restaurant_floor_1.yaml.
"""

from __future__ import annotations

import ast
from pathlib import Path
from PIL import Image, ImageDraw


def parse_map_yaml(yaml_path: Path) -> tuple[str, float, tuple[float, float, float]]:
    data: dict[str, str] = {}
    for line in yaml_path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or ":" not in s:
            continue
        k, v = s.split(":", 1)
        data[k.strip()] = v.strip()
    image_name = data["image"]
    resolution = float(data["resolution"])
    origin = tuple(float(x) for x in ast.literal_eval(data["origin"]))
    return image_name, resolution, (origin[0], origin[1], origin[2])


def world_rect_to_pixel_box(
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    ox: float,
    oy: float,
    res: float,
    width: int,
    height: int,
) -> tuple[int, int, int, int]:
    px0 = max(0, min(width - 1, int((x_min - ox) / res)))
    px1 = max(0, min(width - 1, int((x_max - ox) / res)))
    # Trong PGM ROS 2: row 0 là đỉnh trên (y_max), row H-1 là đáy (y_min = oy)
    py0 = max(0, min(height - 1, height - 1 - int((y_max - oy) / res)))
    py1 = max(0, min(height - 1, height - 1 - int((y_min - oy) / res)))
    return (min(px0, px1), min(py0, py1), max(px0, px1), max(py0, py1))


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    maps_dir = repo_root / "ros2_ws" / "src" / "restaurant_robot_navigation" / "maps"
    base_yaml = maps_dir / "restaurant_floor_1.yaml"
    if not base_yaml.is_file():
        raise FileNotFoundError(f"Chưa có bản đồ SLAM: {base_yaml}")

    image_name, res, (ox, oy, oyaw) = parse_map_yaml(base_yaml)
    base_img = Image.open(maps_dir / image_name)
    width, height = base_img.size

    # 1. Keepout Mask (type 0, trinary: 254=Free, 0=Occupied/Keepout)
    keepout_img = Image.new("L", (width, height), color=254)
    keepout_draw = ImageDraw.Draw(keepout_img)
    keepout_zones = [
        ("Khu bếp nóng", -7.0, -5.3, 0.0, 5.0),
        ("Khu sau quầy lễ tân", 5.1, 7.0, 2.0, 5.0),
    ]
    for label, x0, x1, y0, y1 in keepout_zones:
        box = world_rect_to_pixel_box(x0, x1, y0, y1, ox, oy, res, width, height)
        keepout_draw.rectangle(box, fill=0)
        print(f"Keepout zone [{label}]: world=[{x0},{x1}]x[{y0},{y1}] -> px={box}")

    keepout_pgm = maps_dir / "keepout_mask.pgm"
    keepout_yaml = maps_dir / "keepout_mask.yaml"
    keepout_img.save(keepout_pgm)
    keepout_yaml.write_text(
        "\n".join(
            [
                "image: keepout_mask.pgm",
                "mode: trinary",
                f"resolution: {res}",
                f"origin: [{ox}, {oy}, {oyaw}]",
                "negate: 0",
                "occupied_thresh: 0.65",
                "free_thresh: 0.25",
                "",
            ]
        ),
        encoding="utf-8",
    )

    # 2. Speed Mask (type 1 percent, scale: 255=0->NoLimit/100%, 0=100->base+mult*100=50%)
    speed_img = Image.new("L", (width, height), color=255)
    speed_draw = ImageDraw.Draw(speed_img)
    speed_zones = [
        ("Cửa bếp (giảm 50% tốc độ)", -4.1, -2.7, 1.2, 3.2),
    ]
    for label, x0, x1, y0, y1 in speed_zones:
        box = world_rect_to_pixel_box(x0, x1, y0, y1, ox, oy, res, width, height)
        speed_draw.rectangle(box, fill=0)
        print(f"Speed zone   [{label}]: world=[{x0},{x1}]x[{y0},{y1}] -> px={box}")

    speed_pgm = maps_dir / "speed_mask.pgm"
    speed_yaml = maps_dir / "speed_mask.yaml"
    speed_img.save(speed_pgm)
    speed_yaml.write_text(
        "\n".join(
            [
                "image: speed_mask.pgm",
                "mode: scale",
                f"resolution: {res}",
                f"origin: [{ox}, {oy}, {oyaw}]",
                "negate: 0",
                "occupied_thresh: 1.0",
                "free_thresh: 0.0",
                "",
            ]
        ),
        encoding="utf-8",
    )

    keepout_black = sum(1 for p in keepout_img.getdata() if p == 0)
    speed_black = sum(1 for p in speed_img.getdata() if p == 0)
    print(
        f"[PASS] Generated keepout_mask ({width}x{height}, {keepout_black} keepout px) "
        f"and speed_mask ({width}x{height}, {speed_black} speed-limit px)"
    )


if __name__ == "__main__":
    main()
