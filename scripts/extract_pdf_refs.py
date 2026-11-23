#!/usr/bin/env python3
"""Trích xuất 2 bộ tài liệu PDF trong docs/ thành các file Markdown theo chương cho Workspace Skills.

Cách dùng:
    python3 scripts/extract_pdf_refs.py
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PraSection:
    filename: str
    part: str
    title: str
    pdf_start: int
    pdf_end: int
    priority: str
    summary: str


@dataclass(frozen=True)
class IotSection:
    filename: str
    title: str
    slide_start: int
    slide_end: int
    subsections: str
    project_mapping: str


PRA_FOOTER_RE = re.compile(
    r"This material will be published by Cambridge University Press.*?Marco Pavone 2026\.",
    flags=re.DOTALL,
)

PRA_SECTIONS: list[PraSection] = [
    PraSection(
        "preface.md",
        "Mở đầu",
        "Preface — Định nghĩa Robot Autonomy & Vòng lặp See–Think–Act",
        3,
        10,
        "THAM KHẢO",
        "Tổng quan khái niệm Robot Autonomy, kiến trúc See–Think–Act và bố cục toàn sách.",
    ),
    PraSection(
        "ch00_robot_autonomy_software.md",
        "Nền tảng",
        "Robot Autonomy Software — Nguyên lý phần mềm & ROS",
        17,
        24,
        "CỐT LÕI",
        "Nguyên lý kiến trúc phần mềm robot, ROS nodes/topics/services/actions và tích hợp hệ thống.",
    ),
    PraSection(
        "ch01_modeling_robot_dynamics.md",
        "Part I: Motion Planning & Control",
        "Ch 1: Modeling Robot Dynamics (Wheeled Robot Motion Models)",
        27,
        56,
        "CỐT LÕI",
        "Mô hình không gian trạng thái, động học & động lực học, mô hình xe bánh vi sai (unicycle/diff-drive), ràng buộc Pfaffian.",
    ),
    PraSection(
        "ch02_open_loop_control.md",
        "Part I: Motion Planning & Control",
        "Ch 2: Open-Loop Control & Trajectory Optimization",
        57,
        90,
        "THAM KHẢO",
        "Bài toán điều khiển tối ưu, phương pháp trực tiếp/gián tiếp và hệ phẳng vi phân (differential flatness).",
    ),
    PraSection(
        "ch03_closed_loop_control.md",
        "Part I: Motion Planning & Control",
        "Ch 3: Closed-Loop Control & Trajectory Tracking",
        91,
        128,
        "CỐT LÕI",
        "Điều khiển phản hồi kinh điển (PID), LQR, điều khiển phi tuyến và MPC bám quỹ đạo.",
    ),
    PraSection(
        "ch04_motion_planning.md",
        "Part I: Motion Planning & Control",
        "Ch 4: Motion Planning",
        129,
        160,
        "CỐT LÕI",
        "Bài toán quy hoạch chuyển động: thuật toán lưới (Dijkstra/A*), tổ hợp, lấy mẫu (RRT/PRM) và trường thế năng.",
    ),
    PraSection(
        "ch05_robot_sensors.md",
        "Part II: Robot Perception",
        "Ch 5: Introduction to Robot Sensors",
        163,
        172,
        "CỐT LÕI",
        "Phân loại cảm biến, chỉ số hiệu năng, mô hình sai số/nhiễu (LiDAR, IMU, Encoder, Camera).",
    ),
    PraSection(
        "ch06_camera_models_calibration.md",
        "Part II: Robot Perception",
        "Ch 6: Camera Models and Calibration",
        173,
        194,
        "CỐT LÕI",
        "Mô hình camera lỗ kim, phép chiếu phối cảnh, chuyển đổi tọa độ và hiệu chuẩn camera (nội/ngoại tham) cho AprilTag.",
    ),
    PraSection(
        "ch07_stereo_vision_sfm.md",
        "Part II: Robot Perception",
        "Ch 7: Stereo Vision and Structure From Motion",
        195,
        204,
        "THAM KHẢO",
        "Thị giác lập thể, hình học epipolar và tái tạo 3D (Structure from Motion).",
    ),
    PraSection(
        "ch08_classical_perception.md",
        "Part II: Robot Perception",
        "Ch 8: Classical Methods for Perception",
        205,
        228,
        "HỮU ÍCH",
        "Xử lý ảnh cơ bản, trích xuất đặc trưng hình học (cạnh/góc/đoạn thẳng) và phát hiện đối tượng cổ điển.",
    ),
    PraSection(
        "ch09_deep_learning_perception.md",
        "Part II: Robot Perception",
        "Ch 9: Deep Learning Architectures for Perception",
        229,
        252,
        "THAM KHẢO",
        "Mạng CNN, Transformer, xử lý đám mây điểm 3D (PointNet) và Voxel.",
    ),
    PraSection(
        "ch10_object_detection_recognition.md",
        "Part II: Robot Perception",
        "Ch 10: Object Detection and Recognition",
        253,
        280,
        "THAM KHẢO",
        "Phát hiện vật thể 2D/3D và phân đoạn ngữ nghĩa/thực thể (segmentation).",
    ),
    PraSection(
        "ch11_localization_filtering.md",
        "Part III: Localization & Mapping",
        "Ch 11: Introduction to Localization and Filtering",
        283,
        300,
        "CỐT LÕI",
        "Xác suất nền tảng, mô hình Markov và bộ lọc Bayes tổng quát cho định vị robot.",
    ),
    PraSection(
        "ch12_approximate_filters.md",
        "Part III: Localization & Mapping",
        "Ch 12: Approximate Filters for State Estimation",
        301,
        328,
        "CỐT LÕI",
        "Phân phối Gauss, bộ lọc Kalman (KF), EKF/UKF và bộ lọc hạt (Particle Filter).",
    ),
    PraSection(
        "ch13_robot_localization.md",
        "Part III: Localization & Mapping",
        "Ch 13: Robot Localization",
        329,
        346,
        "CỐT LÕI",
        "Định vị trên bản đồ biết trước: Markov Localization, EKF Localization và Monte Carlo Localization (MCL/AMCL).",
    ),
    PraSection(
        "ch14_slam.md",
        "Part III: Localization & Mapping",
        "Ch 14: Simultaneous Localization and Mapping (SLAM)",
        347,
        392,
        "CỐT LÕI",
        "Mô hình toán SLAM, front-end quét laser, EKF-SLAM, Particle-SLAM, Graph SLAM và Factor Graph SLAM.",
    ),
    PraSection(
        "ch15_sensor_fusion_tracking.md",
        "Part III: Localization & Mapping",
        "Ch 15: Sensor Fusion and Object Tracking",
        393,
        426,
        "CỐT LÕI",
        "Kiến trúc hợp nhất đa cảm biến (EKF Encoder + IMU) và theo dõi vật thể động (người đi bộ trong nhà hàng).",
    ),
    PraSection(
        "ch16_finite_state_machines.md",
        "Part IV: Robot Decision Making",
        "Ch 16: Finite State Machines",
        429,
        438,
        "CỐT LÕI",
        "Mô hình toán máy trạng thái hữu hạn (FSM), thiết kế kiến trúc điều khiển rời rạc và giới hạn của FSM.",
    ),
    PraSection(
        "ch17_sequential_decision_making.md",
        "Part IV: Robot Decision Making",
        "Ch 17: Sequential Decision Making and Dynamic Programming",
        439,
        458,
        "HỮU ÍCH",
        "Quy hoạch động tất định và Markov Decision Processes (MDP) dưới bất định.",
    ),
    PraSection(
        "ch18_reinforcement_learning.md",
        "Part IV: Robot Decision Making",
        "Ch 18: Reinforcement Learning",
        459,
        496,
        "THAM KHẢO",
        "Bài toán học tăng cường (RL), phương pháp model-free và model-based.",
    ),
    PraSection(
        "ch19_imitation_learning.md",
        "Part IV: Robot Decision Making",
        "Ch 19: Imitation Learning",
        497,
        512,
        "THAM KHẢO",
        "Học bắt chước (Behavior Cloning) và Inverse Reinforcement Learning.",
    ),
    PraSection(
        "prospects.md",
        "Tổng kết",
        "Prospects — Xu hướng nghiên cứu Robot Autonomy",
        513,
        520,
        "THAM KHẢO",
        "Tổng quan hành trình công nghệ tự hành và hướng mở rộng tương lai (Physical AI, World Models).",
    ),
    PraSection(
        "bibliography.md",
        "Tài liệu trích dẫn",
        "References — Danh mục tài liệu tham khảo gốc",
        521,
        531,
        "THAM KHẢO",
        "Danh mục bài báo và sách trích dẫn chuẩn học thuật để trích dẫn lại trong luận văn.",
    ),
]

IOT_SECTIONS: list[IotSection] = [
    IotSection(
        "ch01_tong_quan_iot.md",
        "Chương 1: Tổng quan về IoT",
        1,
        60,
        "Giới thiệu môn học (1–4); 1.1 Tổng quan (6–18); 1.2 Kiến trúc (19–22); 1.3 Công nghệ (23–35); 1.4 Ứng dụng (36–52); 1.5 Thách thức (53–60)",
        "Khái niệm hệ thống IoT, mô hình kiến trúc phân lớp (Edge/Gateway/Cloud) dùng chuẩn cho chương Thiết kế hệ thống trong luận văn.",
    ),
    IotSection(
        "ch02a_cam_bien_va_truyen_thong.md",
        "Chương 2 (Phần A): Cảm biến, Thiết bị & Chuẩn truyền thông",
        61,
        91,
        "2.1 Cảm biến và thiết bị IoT (62–81); 2.2 Một số chuẩn truyền thông (82–91)",
        "Phân loại cảm biến/cơ cấu chấp hành và so sánh các chuẩn truyền thông không dây (Wi-Fi, BLE, Zigbee, LoRa) cho ESP32 IoT.",
    ),
    IotSection(
        "ch02b_giao_thuc_mqtt_http_cloud.md",
        "Chương 2 (Phần B): Giao thức IoT (HTTP, MQTT, AMQP) & Cloud Platform",
        92,
        190,
        "2.3 Giao thức ứng dụng IoT: HTTP, MQTT, AMQP (92–178); 2.4 IoT Cloud Platform (179–190)",
        "Cốt lõi cho tầng MQTT Broker (Pub/Sub, QoS 0/1/2, Retain, LWT) và so sánh lý thuyết MQTT vs HTTP trong luận văn.",
    ),
    IotSection(
        "ch03_lap_trinh_iot_va_web_api.md",
        "Chương 3: Lập trình thiết bị IoT, Web API & Platform",
        191,
        291,
        "3.1 Lập trình thiết bị IoT (192–240); 3.2 Xây dựng Web API (241–277); 3.3 Lập trình với IoT Platform (278–291)",
        "Nguyên lý tương tác phần cứng & thiết kế REST/WebSocket API. Lưu ý: code mẫu Java/ThingSpeak chỉ dùng tham khảo khái niệm, dự án code bằng Rust/ESP32.",
    ),
    IotSection(
        "ch04_an_toan_bao_mat_iot.md",
        "Chương 4: An toàn và Bảo mật IoT",
        292,
        314,
        "4.1 Tổng quan bảo mật IoT (293–295); 4.2 Các dạng tấn công hạ tầng IoT (296–302); 4.3 Các điểm yếu bảo mật IoT (303–314)",
        "Rất quan trọng khi thiết kế bảo mật VPS/Mosquitto: TLS/MQTTS, password & ACL, bảo vệ API và phân tích rủi ro trong luận văn.",
    ),
    IotSection(
        "ch05_thiet_ke_he_thong_iot.md",
        "Chương 5: Thiết kế và Xây dựng Hệ thống IoT",
        315,
        349,
        "Quy trình phân tích yêu cầu, thiết kế kiến trúc, lựa chọn phần cứng/giao thức và triển khai hệ thống IoT",
        "Áp dụng quy trình thiết kế hệ thống IoT đầu-cuối cho hệ thống nhà hàng thông minh (Robot + Bàn + Smart Dock + Server).",
    ),
]


def extract_pdf_pages(pdf_path: Path) -> list[str]:
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file PDF: {pdf_path}")
    res = subprocess.run(
        ["pdftotext", str(pdf_path), "-"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    pages = res.stdout.split("\f")
    if pages and pages[-1].strip() == "":
        pages = pages[:-1]
    return pages


def clean_whitespace(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned = "\n".join(lines).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def clean_pra_page(raw_page: str) -> str:
    no_footer = PRA_FOOTER_RE.sub("", raw_page)
    return clean_whitespace(no_footer)


def approx_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def build_pra_references(repo_root: Path) -> tuple[int, int]:
    pdf_path = repo_root / "docs" / "2608.03496v2.pdf"
    ref_dir = repo_root / ".agents" / "skills" / "robot-autonomy-ref" / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)

    pages = extract_pdf_pages(pdf_path)
    if len(pages) != 531:
        raise RuntimeError(f"Kỳ vọng 531 trang ở 2608.03496v2.pdf, nhưng đọc được {len(pages)} trang.")

    index_rows: list[str] = []
    total_tokens = 0

    for sec in PRA_SECTIONS:
        book_start = sec.pdf_start - 2
        book_end = sec.pdf_end - 2
        parts: list[str] = [
            f"# {sec.title}",
            "",
            f"- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)",
            f"- **Phần:** {sec.part}",
            f"- **Trang sách:** {book_start}–{book_end} | **Trang PDF:** {sec.pdf_start}–{sec.pdf_end}",
            f"- **Độ ưu tiên cho dự án:** `{sec.priority}`",
            f"- **Tóm tắt:** {sec.summary}",
            "",
        ]
        for pdf_p in range(sec.pdf_start, sec.pdf_end + 1):
            book_p = pdf_p - 2
            body = clean_pra_page(pages[pdf_p - 1])
            parts.append("---")
            parts.append("")
            parts.append(f"### [PDF p.{pdf_p} | Book p.{book_p}]")
            parts.append("")
            if body:
                parts.append(body)
            else:
                parts.append("> [Trang ít chữ / trang hình minh họa — xem trực tiếp PDF gốc nếu cần]")
            parts.append("")

        content = "\n".join(parts)
        (ref_dir / sec.filename).write_text(content, encoding="utf-8")

        tok = approx_tokens(content)
        total_tokens += tok
        index_rows.append(
            f"| [{sec.filename}](./{sec.filename}) | {sec.part} | {sec.title} | "
            f"{book_start}–{book_end} | {sec.pdf_start}–{sec.pdf_end} | ~{tok:,} | "
            f"**{sec.priority}** | {sec.summary} |"
        )

    index_md = "\n".join(
        [
            "# Mục Lục Tài Liệu: Principles of Robot Autonomy (`2608.03496v2.pdf`)",
            "",
            "- **Tác giả:** Daniele Gammelli, Joseph Lorenzetti, Katie Luo, Gioele Zardini, Marco Pavone (Cambridge University Press / Stanford AA274A, 2026)",
            f"- **Tổng số phần đã tách:** {len(PRA_SECTIONS)} files (từ 531 trang PDF; ước lượng ~{total_tokens:,} tokens toàn bộ)",
            "- **Quy tắc ánh xạ trang:** `Book p.X = PDF p.(X + 2)` (ví dụ Chương 14 SLAM bắt đầu tại Book p.345 → PDF p.347).",
            "- **Ghi chú:** Toàn bộ footer bản quyền lặp lại đã được lọc sạch để giảm nhiễu ngữ cảnh.",
            "",
            "## Xem Lại Công Thức / Hình Vẽ Gốc Từ PDF (Khi Cần)",
            "",
            "Khi plain-text ở một trang có công thức ma trận hoặc sơ đồ phức tạp bị mất định dạng, xuất đúng trang `[PDF p.XX]` thành ảnh PNG và đọc bằng `read_file`:",
            "",
            "```bash",
            "pdftoppm -f XX -l XX -png -r 150 /home/vuloi/prj/robot/docs/2608.03496v2.pdf /tmp/pra_page",
            "```",
            "",
            "## Danh Sách Chương & Mức Độ Ưu Tiên",
            "",
            "| File | Phần | Tiêu đề | Trang sách | Trang PDF | ~Tokens | Ưu tiên | Nội dung cốt lõi |",
            "| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |",
            *index_rows,
            "",
        ]
    )
    (ref_dir / "INDEX.md").write_text(index_md, encoding="utf-8")
    return len(PRA_SECTIONS), total_tokens


def build_iot_references(repo_root: Path) -> tuple[int, int]:
    pdf_path = repo_root / "docs" / "it4735_iot_va_ung_dung_v2025_16.1m.pdf"
    ref_dir = repo_root / ".agents" / "skills" / "iot-hust-ref" / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)

    pages = extract_pdf_pages(pdf_path)
    if len(pages) != 349:
        raise RuntimeError(
            f"Kỳ vọng 349 slides ở it4735_iot_va_ung_dung_v2025_16.1m.pdf, nhưng đọc được {len(pages)} slides."
        )

    index_rows: list[str] = []
    total_tokens = 0

    for sec in IOT_SECTIONS:
        sparse_count = 0
        parts: list[str] = [
            f"# {sec.title}",
            "",
            "- **PDF gốc:** `docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf` (*IT4735 IoT và Ứng dụng*, SoICT - HUST, 2025)",
            f"- **Phạm vi slide:** {sec.slide_start}–{sec.slide_end}",
            f"- **Các mục lớn:** {sec.subsections}",
            f"- **Ứng dụng vào dự án Robot Nhà Hàng:** {sec.project_mapping}",
            "",
        ]
        for slide_no in range(sec.slide_start, sec.slide_end + 1):
            body = clean_whitespace(pages[slide_no - 1])
            parts.append("---")
            parts.append("")
            parts.append(f"### [Slide {slide_no}]")
            parts.append("")
            if len(body) < 50:
                sparse_count += 1
                if body:
                    parts.append(body)
                    parts.append("")
                parts.append(
                    f"> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide {slide_no} trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]"
                )
            else:
                parts.append(body)
            parts.append("")

        content = "\n".join(parts)
        (ref_dir / sec.filename).write_text(content, encoding="utf-8")

        tok = approx_tokens(content)
        total_tokens += tok
        index_rows.append(
            f"| [{sec.filename}](./{sec.filename}) | {sec.slide_start}–{sec.slide_end} | "
            f"{sec.subsections} | {sparse_count} | ~{tok:,} | {sec.project_mapping} |"
        )

    index_md = "\n".join(
        [
            "# Mục Lục Tài Liệu: IT4735 — IoT và Ứng Dụng (`it4735_iot_va_ung_dung_v2025_16.1m.pdf`)",
            "",
            "- **Nguồn:** Phạm Ngọc Hưng, Nguyễn Đình Thuận, Đặng Tuấn Linh — Trường CNTT&TT (SoICT), ĐH Bách khoa Hà Nội (2025)",
            f"- **Tổng số phần đã tách:** {len(IOT_SECTIONS)} files (từ 349 slides PDF; ước lượng ~{total_tokens:,} tokens toàn bộ)",
            "",
            "## Lưu Ý Khi Tham Chiếu Cho Dự Án Robot Nhà Hàng",
            "",
            "1. **Không chép code Java / ThingSpeak trong slide:** Slide dùng Java/ThingSpeak cho mục đích giảng dạy đại cương; khi code cho dự án luôn giữ đúng stack đã chốt (**Rust Axum + rumqttc + Mosquitto + ESP32/STM32 + ROS 2 Jazzy**).",
            "2. **Slide sơ đồ/hình vẽ (`< 50` ký tự text):** Khi gặp ghi chú `[Slide hình ảnh/sơ đồ]`, có thể xuất đúng slide đó bằng `pdftoppm` và xem bằng `read_file`:",
            "",
            "```bash",
            "pdftoppm -f XX -l XX -png -r 150 /home/vuloi/prj/robot/docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf /tmp/iot_slide",
            "```",
            "",
            "## Danh Sách Chương & Ánh Xạ Dự Án",
            "",
            "| File | Slides | Các mục lớn | Slide ít chữ/sơ đồ | ~Tokens | Ứng dụng trực tiếp vào dự án |",
            "| :--- | :---: | :--- | :---: | :---: | :--- |",
            *index_rows,
            "",
        ]
    )
    (ref_dir / "INDEX.md").write_text(index_md, encoding="utf-8")
    return len(IOT_SECTIONS), total_tokens


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    pra_count, pra_tokens = build_pra_references(repo_root)
    iot_count, iot_tokens = build_iot_references(repo_root)
    print(f"robot-autonomy-ref: {pra_count} files + INDEX.md (~{pra_tokens:,} tokens)")
    print(f"iot-hust-ref      : {iot_count} files + INDEX.md (~{iot_tokens:,} tokens)")


if __name__ == "__main__":
    main()
