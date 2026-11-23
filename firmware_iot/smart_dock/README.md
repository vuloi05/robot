# Trạm Sạc Thông Minh (ESP32 Smart Dock)

Thiết bị gắn trên trạm sạc (có biển AprilTag `tag36h11` và tiếp điểm sạc từ tính Magnetic Pogo Pins).

## Chức năng
- Đo điện áp và dòng sạc thực tế qua `INA219/INA226`.
- Theo dõi nhiệt độ tiếp điểm sạc.
- Báo trạng thái trạm sạc (`FREE`, `OCCUPIED`, `CHARGING`, `FAULT`) về topic `dock/{dock_id}/status` (QoS 1, Retain=true, LWT).

> Triển khai hoàn thiện ở **Giai đoạn 5**.
