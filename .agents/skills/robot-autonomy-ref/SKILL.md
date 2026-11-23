---
name: robot-autonomy-ref
description: >-
  Authoritative textbook reference from Principles of Robot Autonomy (Gammelli et al., 2026)
  covering wheeled robot dynamics, PID/LQR/MPC trajectory tracking, motion planning (A*, RRT,
  potential fields), robot sensors (LiDAR, IMU), pinhole camera calibration for AprilTag docking,
  Bayes/Kalman/EKF/Particle filtering, AMCL localization, Graph/Factor-Graph SLAM, sensor fusion,
  and finite state machines. Use this skill when designing, tuning, or debugging kinematics,
  controllers, Nav2 planners, EKF/AMCL/SLAM, camera calibration, mission FSMs, or drafting
  theoretical foundations for the thesis.
---

# Principles of Robot Autonomy — Tài Liệu Tham Chiếu Robotics

Bộ tham chiếu tách từ giáo trình *Principles of Robot Autonomy* ([2608.03496v2.pdf](../../../docs/2608.03496v2.pdf), 531 trang) dành cho phần **Lý thuyết tự hành, Điều hướng & Điều khiển** của dự án Robot Phục Vụ Nhà Hàng.

## Quy Trình Tra Cứu 3 Bước (Progressive Disclosure)

1. **Bước 1 — Đọc mục lục trước:** Luôn đọc [references/INDEX.md](references/INDEX.md) (hoặc tra bảng ánh xạ nhanh bên dưới) để xác định đúng chương cần dùng. **Không** đọc hàng loạt chương không liên quan.
2. **Bước 2 — Đọc đúng 1–2 file chương cần thiết:** Mở file tương ứng trong `references/` (dùng `read_file` theo `StartLine`/`EndLine` hoặc tìm từ khóa theo mốc `[PDF p.XX | Book p.YY]`).
3. **Bước 3 — Xem lại công thức toán / sơ đồ gốc (nếu cần):** Nếu công thức ma trận nhiều tầng hoặc sơ đồ ở bản text thuần bị mất định dạng, dùng `pdftoppm` xuất đúng trang `[PDF p.XX]` thành PNG rồi kiểm tra bằng `read_file`:
   ```bash
   pdftoppm -f XX -l XX -png -r 150 /home/vuloi/prj/robot/docs/2608.03496v2.pdf /tmp/pra_page
   ```

## Bảng Ánh Xạ Nhanh: Module Dự Án ↔ Chương Sách

| Thành phần trong `/home/vuloi/prj/robot` | Chương tham chiếu ưu tiên | Trọng tâm áp dụng |
| :--- | :--- | :--- |
| Kiến trúc chung ROS 2 (`ros2_ws/`) | [references/ch00_robot_autonomy_software.md](references/ch00_robot_autonomy_software.md) | Nodes, Topics, Services, Actions, See–Think–Act |
| Động học vi sai (`diff_drive`, Odometry, STM32) | [references/ch01_modeling_robot_dynamics.md](references/ch01_modeling_robot_dynamics.md) | Mô hình Unicycle / Differential Drive, ràng buộc Pfaffian |
| PID động cơ STM32 & `velocity_smoother` | [references/ch03_closed_loop_control.md](references/ch03_closed_loop_control.md) | Phản hồi PID, LQR, MPC bám quỹ đạo mượt |
| Nav2 Global Planner & tránh vật cản | [references/ch04_motion_planning.md](references/ch04_motion_planning.md) | Tìm đường lưới (A*/Dijkstra), RRT, trường thế năng |
| Mô hình nhiễu LiDAR 2D / IMU / Encoder | [references/ch05_robot_sensors.md](references/ch05_robot_sensors.md) | Sai số ngẫu nhiên/hệ thống, băng thông, hiệu chuẩn |
| Camera USB & `apriltag_ros` (`opennav_docking`) | [references/ch06_camera_models_calibration.md](references/ch06_camera_models_calibration.md) | Phép chiếu phối cảnh, ma trận nội tham $K$, ngoại tham $[R\|t]$ |
| Bộ lọc Bayes, Kalman, EKF, Particle Filter | [references/ch11_localization_filtering.md](references/ch11_localization_filtering.md) & [references/ch12_approximate_filters.md](references/ch12_approximate_filters.md) | Nền tảng toán học cho `robot_localization` & AMCL |
| Định vị AMCL (`nav2_amcl`) | [references/ch13_robot_localization.md](references/ch13_robot_localization.md) | Monte Carlo Localization (MCL) trên bản đồ 2D |
| Lập bản đồ `slam_toolbox` | [references/ch14_slam.md](references/ch14_slam.md) | Scan-matching front-end, Graph SLAM, Factor Graph |
| Hợp nhất Encoder + IMU (`EKF`) & theo dõi người | [references/ch15_sensor_fusion_tracking.md](references/ch15_sensor_fusion_tracking.md) | Kiến trúc Sensor Fusion & Object Tracking |
| Máy trạng thái `mission_manager` (`fsm_states.py`) | [references/ch16_finite_state_machines.md](references/ch16_finite_state_machines.md) | Thiết kế FSM chuẩn hóa, ưu/nhược điểm FSM |
