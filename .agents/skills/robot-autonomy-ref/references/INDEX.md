# Mục Lục Tài Liệu: Principles of Robot Autonomy (`2608.03496v2.pdf`)

- **Tác giả:** Daniele Gammelli, Joseph Lorenzetti, Katie Luo, Gioele Zardini, Marco Pavone (Cambridge University Press / Stanford AA274A, 2026)
- **Tổng số phần đã tách:** 23 files (từ 531 trang PDF; ước lượng ~303,737 tokens toàn bộ)
- **Quy tắc ánh xạ trang:** `Book p.X = PDF p.(X + 2)` (ví dụ Chương 14 SLAM bắt đầu tại Book p.345 → PDF p.347).
- **Ghi chú:** Toàn bộ footer bản quyền lặp lại đã được lọc sạch để giảm nhiễu ngữ cảnh.

## Xem Lại Công Thức / Hình Vẽ Gốc Từ PDF (Khi Cần)

Khi plain-text ở một trang có công thức ma trận hoặc sơ đồ phức tạp bị mất định dạng, xuất đúng trang `[PDF p.XX]` thành ảnh PNG và đọc bằng `read_file`:

```bash
pdftoppm -f XX -l XX -png -r 150 /home/vuloi/prj/robot/docs/2608.03496v2.pdf /tmp/pra_page
```

## Danh Sách Chương & Mức Độ Ưu Tiên

| File | Phần | Tiêu đề | Trang sách | Trang PDF | ~Tokens | Ưu tiên | Nội dung cốt lõi |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| [preface.md](./preface.md) | Mở đầu | Preface — Định nghĩa Robot Autonomy & Vòng lặp See–Think–Act | 1–8 | 3–10 | ~4,966 | **THAM KHẢO** | Tổng quan khái niệm Robot Autonomy, kiến trúc See–Think–Act và bố cục toàn sách. |
| [ch00_robot_autonomy_software.md](./ch00_robot_autonomy_software.md) | Nền tảng | Robot Autonomy Software — Nguyên lý phần mềm & ROS | 15–22 | 17–24 | ~3,682 | **CỐT LÕI** | Nguyên lý kiến trúc phần mềm robot, ROS nodes/topics/services/actions và tích hợp hệ thống. |
| [ch01_modeling_robot_dynamics.md](./ch01_modeling_robot_dynamics.md) | Part I: Motion Planning & Control | Ch 1: Modeling Robot Dynamics (Wheeled Robot Motion Models) | 25–54 | 27–56 | ~17,944 | **CỐT LÕI** | Mô hình không gian trạng thái, động học & động lực học, mô hình xe bánh vi sai (unicycle/diff-drive), ràng buộc Pfaffian. |
| [ch02_open_loop_control.md](./ch02_open_loop_control.md) | Part I: Motion Planning & Control | Ch 2: Open-Loop Control & Trajectory Optimization | 55–88 | 57–90 | ~18,359 | **THAM KHẢO** | Bài toán điều khiển tối ưu, phương pháp trực tiếp/gián tiếp và hệ phẳng vi phân (differential flatness). |
| [ch03_closed_loop_control.md](./ch03_closed_loop_control.md) | Part I: Motion Planning & Control | Ch 3: Closed-Loop Control & Trajectory Tracking | 89–126 | 91–128 | ~22,549 | **CỐT LÕI** | Điều khiển phản hồi kinh điển (PID), LQR, điều khiển phi tuyến và MPC bám quỹ đạo. |
| [ch04_motion_planning.md](./ch04_motion_planning.md) | Part I: Motion Planning & Control | Ch 4: Motion Planning | 127–158 | 129–160 | ~20,886 | **CỐT LÕI** | Bài toán quy hoạch chuyển động: thuật toán lưới (Dijkstra/A*), tổ hợp, lấy mẫu (RRT/PRM) và trường thế năng. |
| [ch05_robot_sensors.md](./ch05_robot_sensors.md) | Part II: Robot Perception | Ch 5: Introduction to Robot Sensors | 161–170 | 163–172 | ~5,658 | **CỐT LÕI** | Phân loại cảm biến, chỉ số hiệu năng, mô hình sai số/nhiễu (LiDAR, IMU, Encoder, Camera). |
| [ch06_camera_models_calibration.md](./ch06_camera_models_calibration.md) | Part II: Robot Perception | Ch 6: Camera Models and Calibration | 171–192 | 173–194 | ~11,417 | **CỐT LÕI** | Mô hình camera lỗ kim, phép chiếu phối cảnh, chuyển đổi tọa độ và hiệu chuẩn camera (nội/ngoại tham) cho AprilTag. |
| [ch07_stereo_vision_sfm.md](./ch07_stereo_vision_sfm.md) | Part II: Robot Perception | Ch 7: Stereo Vision and Structure From Motion | 193–202 | 195–204 | ~5,605 | **THAM KHẢO** | Thị giác lập thể, hình học epipolar và tái tạo 3D (Structure from Motion). |
| [ch08_classical_perception.md](./ch08_classical_perception.md) | Part II: Robot Perception | Ch 8: Classical Methods for Perception | 203–226 | 205–228 | ~13,358 | **HỮU ÍCH** | Xử lý ảnh cơ bản, trích xuất đặc trưng hình học (cạnh/góc/đoạn thẳng) và phát hiện đối tượng cổ điển. |
| [ch09_deep_learning_perception.md](./ch09_deep_learning_perception.md) | Part II: Robot Perception | Ch 9: Deep Learning Architectures for Perception | 227–250 | 229–252 | ~15,606 | **THAM KHẢO** | Mạng CNN, Transformer, xử lý đám mây điểm 3D (PointNet) và Voxel. |
| [ch10_object_detection_recognition.md](./ch10_object_detection_recognition.md) | Part II: Robot Perception | Ch 10: Object Detection and Recognition | 251–278 | 253–280 | ~17,401 | **THAM KHẢO** | Phát hiện vật thể 2D/3D và phân đoạn ngữ nghĩa/thực thể (segmentation). |
| [ch11_localization_filtering.md](./ch11_localization_filtering.md) | Part III: Localization & Mapping | Ch 11: Introduction to Localization and Filtering | 281–298 | 283–300 | ~9,438 | **CỐT LÕI** | Xác suất nền tảng, mô hình Markov và bộ lọc Bayes tổng quát cho định vị robot. |
| [ch12_approximate_filters.md](./ch12_approximate_filters.md) | Part III: Localization & Mapping | Ch 12: Approximate Filters for State Estimation | 299–326 | 301–328 | ~14,740 | **CỐT LÕI** | Phân phối Gauss, bộ lọc Kalman (KF), EKF/UKF và bộ lọc hạt (Particle Filter). |
| [ch13_robot_localization.md](./ch13_robot_localization.md) | Part III: Localization & Mapping | Ch 13: Robot Localization | 327–344 | 329–346 | ~9,426 | **CỐT LÕI** | Định vị trên bản đồ biết trước: Markov Localization, EKF Localization và Monte Carlo Localization (MCL/AMCL). |
| [ch14_slam.md](./ch14_slam.md) | Part III: Localization & Mapping | Ch 14: Simultaneous Localization and Mapping (SLAM) | 345–390 | 347–392 | ~27,182 | **CỐT LÕI** | Mô hình toán SLAM, front-end quét laser, EKF-SLAM, Particle-SLAM, Graph SLAM và Factor Graph SLAM. |
| [ch15_sensor_fusion_tracking.md](./ch15_sensor_fusion_tracking.md) | Part III: Localization & Mapping | Ch 15: Sensor Fusion and Object Tracking | 391–424 | 393–426 | ~20,825 | **CỐT LÕI** | Kiến trúc hợp nhất đa cảm biến (EKF Encoder + IMU) và theo dõi vật thể động (người đi bộ trong nhà hàng). |
| [ch16_finite_state_machines.md](./ch16_finite_state_machines.md) | Part IV: Robot Decision Making | Ch 16: Finite State Machines | 427–436 | 429–438 | ~5,196 | **CỐT LÕI** | Mô hình toán máy trạng thái hữu hạn (FSM), thiết kế kiến trúc điều khiển rời rạc và giới hạn của FSM. |
| [ch17_sequential_decision_making.md](./ch17_sequential_decision_making.md) | Part IV: Robot Decision Making | Ch 17: Sequential Decision Making and Dynamic Programming | 437–456 | 439–458 | ~11,252 | **HỮU ÍCH** | Quy hoạch động tất định và Markov Decision Processes (MDP) dưới bất định. |
| [ch18_reinforcement_learning.md](./ch18_reinforcement_learning.md) | Part IV: Robot Decision Making | Ch 18: Reinforcement Learning | 457–494 | 459–496 | ~24,582 | **THAM KHẢO** | Bài toán học tăng cường (RL), phương pháp model-free và model-based. |
| [ch19_imitation_learning.md](./ch19_imitation_learning.md) | Part IV: Robot Decision Making | Ch 19: Imitation Learning | 495–510 | 497–512 | ~11,060 | **THAM KHẢO** | Học bắt chước (Behavior Cloning) và Inverse Reinforcement Learning. |
| [prospects.md](./prospects.md) | Tổng kết | Prospects — Xu hướng nghiên cứu Robot Autonomy | 511–518 | 513–520 | ~6,044 | **THAM KHẢO** | Tổng quan hành trình công nghệ tự hành và hướng mở rộng tương lai (Physical AI, World Models). |
| [bibliography.md](./bibliography.md) | Tài liệu trích dẫn | References — Danh mục tài liệu tham khảo gốc | 519–529 | 521–531 | ~6,561 | **THAM KHẢO** | Danh mục bài báo và sách trích dẫn chuẩn học thuật để trích dẫn lại trong luận văn. |
