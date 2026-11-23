# Nút Gọi Bàn Vật Lý (ESP32 IoT Node)

Thiết bị gắn tại bàn ăn giúp khách hoặc nhân viên bấm gọi robot thu dọn/hỗ trợ và nhận phản hồi qua đèn LED.

## Giao tiếp MQTT (`docs/mqtt_protocol.md`)
- **Publish:** `table/{table_id}/call` (QoS 1, `source: "esp32_button"`)
- **Subscribe:** `table/{table_id}/led` (`IDLE`, `QUEUED`, `ROBOT_COMING`, `ROBOT_ARRIVED`, `ERROR`)

> Triển khai hoàn thiện ở **Giai đoạn 4**.
