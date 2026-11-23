# Firmware ESP32 Tầng Trên Robot (Tray, LED, ToF & MQTT Supervisor)

MCU tầng trên (**ESP32-S3 / ESP32 DevKit**) đảm nhiệm toàn bộ ngoại vi khu vực khay đồ ăn và kênh giám sát dự phòng out-of-band theo kiến trúc Cách B.

## Nhiệm vụ chính
1. **Cảm biến khay (Khay 1 & Khay 2):** Đọc cảm biến tiệm cận hồng ngoại (IR) hoặc Loadcell + HX711 để phát hiện khách đã lấy món.
2. **Dải LED chỉ thị (`WS2812B`):** Hiển thị màu riêng cho Khay 1, Khay 2 và viền trạng thái robot mà không làm ảnh hưởng chu kỳ PID ở STM32 tầng đáy.
3. **Cảm biến tầm gần (`VL53L0X` ToF):** Bù điểm mù phía trên LiDAR để tránh va quệt mặt bàn.
4. **Giao tiếp Pi 5 (`/dev/robot_esp32`):** UART/USB Serial `115200 bps` dùng chung chuẩn [serial_protocol.h](include/serial_protocol.h).
5. **Kênh MQTT Supervisor (`robot/{id}/supervisor`):** Nếu Pi 5 treo hoặc tắt nguồn khi đang sạc (`CMD_PI_HEARTBEAT` quá `5000 ms`), ESP32 vẫn gửi trạng thái pin/khay/E-Stop lên Mosquitto qua Wi-Fi.

> Triển khai code đầy đủ ở **Giai đoạn 5**.
