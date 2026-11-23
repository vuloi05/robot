# Đặc Tả Giao Thức MQTT (Contract v1)

Tài liệu này là **hợp đồng giao tiếp chuẩn duy nhất** giữa:
- `restaurant_mqtt_bridge` (Tầng 4 — ROS 2 trên robot)
- `firmware_robot_esp32` (Tầng 2 — Supervisor tầng trên robot)
- `firmware_iot` (Tầng 2 — Nút gọi bàn & Trạm sạc thông minh)
- `server` (Tầng 5 — Rust IoT Gateway & Fleet Dispatcher)

---

## 1. Quy Ước Chung

- **Broker:** Eclipse Mosquitto 2.x (`infra/docker-compose.yml`).
  - Mạng LAN nội bộ: TCP port `1883`, WebSocket port `9001`.
  - Mạng VPS / Production: MQTTS TLS port `8883` kèm username/password & ACL (`infra/mosquitto/config/acl.example`).
- **Định dạng Payload:** UTF-8 JSON.
- **Trường bắt buộc trong mọi JSON payload:**
  - `"schema_version": 1` (integer)
  - `"ts_ms": <uint64>` (Unix timestamp theo mili-giây UTC)
- **Định danh thiết bị:**
  - `robot_id`: `robot_01`, `robot_02`, ...
  - `table_id`: `table_01`, `table_02`, ... (trùng với `waypoint_id` bàn ăn)
  - `dock_id`: `dock_01`, ...

---

## 2. Bảng Tổng Hợp Topics

| Topic | Hướng gửi | QoS | Retain | LWT | Tần suất / Kích hoạt |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `robot/{robot_id}/status` | Robot Bridge → Broker | 1 | `true` | Có | Khi kết nối / ngắt kết nối |
| `robot/{robot_id}/telemetry` | Robot Bridge → Broker | 0 | `false` | Không | 2–5 Hz định kỳ |
| `robot/{robot_id}/cmd` | Server → Robot Bridge | 1 | `false` | Không | Khi có lệnh mới |
| `robot/{robot_id}/cmd_ack` | Robot Bridge → Server | 1 | `false` | Không | Ngay khi nhận `cmd` |
| `robot/{robot_id}/event` | Robot Bridge → Server | 1 | `false` | Không | Theo sự kiện chuyển trạng thái |
| `robot/{robot_id}/supervisor` | ESP32 Tầng Trên → Broker | 1 | `true` | Có | 0.5–1 Hz hoặc khi có sự cố |
| `table/{table_id}/call` | ESP32 Bàn / Web → Server | 1 | `false` | Không | Khi bấm nút gọi / hủy |
| `table/{table_id}/led` | Server → ESP32 Bàn | 1 | `true` | Không | Khi trạng thái phục vụ đổi |
| `dock/{dock_id}/status` | ESP32 Dock → Broker | 1 | `true` | Có | 1 Hz khi sạc / khi đổi trạng thái |

---

## 3. Chi Tiết Payload Từng Topic

### 3.1. `robot/{robot_id}/status` (Online / Offline + LWT)
Khi kết nối Broker, `restaurant_mqtt_bridge` đăng ký **Last Will and Testament (LWT)** trên chính topic này với `qos=1, retain=true`:

**Payload online (gửi ngay sau khi connect):**
```json
{
  "schema_version": 1,
  "robot_id": "robot_01",
  "online": true,
  "mode": "sim",
  "firmware_version": "0.1.0",
  "ts_ms": 1795400000000
}
```

**Payload LWT (Broker tự phát nếu robot mất kết nối đột ngột):**
```json
{
  "schema_version": 1,
  "robot_id": "robot_01",
  "online": false,
  "mode": "unknown",
  "firmware_version": "0.1.0",
  "ts_ms": 0
}
```

---

### 3.2. `robot/{robot_id}/telemetry` (QoS 0, 2–5 Hz)
```json
{
  "schema_version": 1,
  "robot_id": "robot_01",
  "pose": {
    "map_id": "restaurant_floor_1",
    "x": 2.45,
    "y": -1.18,
    "yaw": 1.57
  },
  "velocity": {
    "vx": 0.35,
    "omega": 0.02
  },
  "battery": {
    "voltage_v": 13.12,
    "current_a": -1.85,
    "pct": 82.5,
    "is_charging": false
  },
  "fsm_state": "DELIVERING",
  "active_task_id": "task_20261123_0012",
  "current_target": "table_02",
  "trays": [
    {
      "tray_id": 1,
      "occupied": true,
      "weight_g": 450,
      "assigned_table": "table_02"
    },
    {
      "tray_id": 2,
      "occupied": true,
      "weight_g": 320,
      "assigned_table": "table_05"
    }
  ],
  "safety": {
    "estop": false,
    "obstacle_blocked": false,
    "tof_front_mm": 1200
  },
  "ts_ms": 1795400001200
}
```

**Giá trị hợp lệ của `fsm_state`:**
`CHARGING`, `IDLE`, `GO_KITCHEN`, `LOADING_FOOD`, `DELIVERING`, `WAITING_PICKUP`, `GO_RECEPTION`, `GREETING_GUEST`, `ESCORTING`, `ARRIVED_ESCORT`, `GO_TABLE_BUS`, `LOADING_DISHES`, `GO_DISHWASH`, `DOCKING`, `BLOCKED`, `ERROR`, `ESTOP`.

---

### 3.3. `robot/{robot_id}/cmd` (Server → Robot, QoS 1)
```json
{
  "schema_version": 1,
  "cmd_id": "cmd_9b1deb4d",
  "task_id": "task_20261123_0012",
  "type": "DELIVERY",
  "priority": 70,
  "speed_profile": "SMOOTH_LIQUID",
  "stops": [
    {
      "stop_index": 0,
      "waypoint_id": "table_02",
      "tray_ids": [1],
      "voice_message": "Mời quý khách bàn 2 nhận món ở khay số 1",
      "wait_timeout_sec": 120
    },
    {
      "stop_index": 1,
      "waypoint_id": "table_05",
      "tray_ids": [2],
      "voice_message": "Mời quý khách bàn 5 nhận món ở khay số 2",
      "wait_timeout_sec": 120
    }
  ],
  "ts_ms": 1795400000500
}
```

- **`type` hợp lệ:** `DELIVERY`, `ESCORT`, `BUSSING`, `DOCK`, `UNDOCK`, `RETURN_HOME`, `CANCEL`, `ESTOP`, `CONFIRM_PICKUP`.
- **`speed_profile` hợp lệ:** `NORMAL`, `ESCORT_SLOW`, `SMOOTH_LIQUID`.
- **Quy tắc Idempotency:** Robot Bridge lưu cache `cmd_id` gần nhất (tối thiểu 64 ID). Nếu nhận trùng `cmd_id` do QoS 1 truyền lại khi rớt gói ACK, robot chỉ gửi lại `cmd_ack` mà **không thực thi lại nhiệm vụ**.

---

### 3.4. `robot/{robot_id}/cmd_ack` (Robot → Server, QoS 1)
```json
{
  "schema_version": 1,
  "robot_id": "robot_01",
  "cmd_id": "cmd_9b1deb4d",
  "task_id": "task_20261123_0012",
  "accepted": true,
  "reason": "OK",
  "ts_ms": 1795400000540
}
```

---

### 3.5. `robot/{robot_id}/event` (Robot → Server, QoS 1)
```json
{
  "schema_version": 1,
  "robot_id": "robot_01",
  "task_id": "task_20261123_0012",
  "event_type": "ARRIVED_WAYPOINT",
  "waypoint_id": "table_02",
  "tray_ids": [1],
  "message": "Robot đã tới bàn 2, đang chờ khách lấy món",
  "ts_ms": 1795400018000
}
```

**`event_type` hợp lệ:**
- `TASK_STARTED`
- `ARRIVED_WAYPOINT`
- `WAITING_PICKUP`
- `PICKUP_CONFIRMED`
- `TASK_COMPLETED`
- `TASK_FAILED`
- `BLOCKED_WARNING` (chắn đường `> 5 s`)
- `BLOCKED_STUCK` (kẹt `> 30 s`)
- `DOCKING_STARTED`
- `DOCKED_CHARGING`
- `LOW_BATTERY`
- `ESTOP_TRIGGERED`

---

### 3.6. `robot/{robot_id}/supervisor` (ESP32 Tầng Trên → Broker, QoS 1, Retain=true, LWT)
Kênh dự phòng **out-of-band** đảm bảo Server vẫn thấy trạng thái nguồn/khay/E-Stop ngay cả khi Raspberry Pi 5 bị treo hoặc tắt nguồn trong lúc robot đang sạc:

```json
{
  "schema_version": 1,
  "robot_id": "robot_01",
  "online": true,
  "pi_alive": true,
  "battery_voltage_v": 13.10,
  "battery_pct": 82.0,
  "trays": [
    { "tray_id": 1, "occupied": true, "weight_g": 450, "assigned_table": "table_02" },
    { "tray_id": 2, "occupied": false, "weight_g": 0, "assigned_table": null }
  ],
  "estop": false,
  "ts_ms": 1795400002000
}
```

---

### 3.7. `table/{table_id}/call` (ESP32 Bàn / QR Web → Server, QoS 1)
```json
{
  "schema_version": 1,
  "call_id": "call_t02_17954000",
  "table_id": "table_02",
  "action": "BUSSING",
  "source": "esp32_button",
  "ts_ms": 1795400025000
}
```
- **`action` hợp lệ:** `BUSSING` (gọi robot thu dọn), `CALL_STAFF` (gọi nhân viên), `CANCEL` (hủy lệnh gọi).
- **`source` hợp lệ:** `esp32_button`, `qr_web`.

---

### 3.8. `table/{table_id}/led` (Server → ESP32 Bàn, QoS 1, Retain=true)
```json
{
  "schema_version": 1,
  "table_id": "table_02",
  "mode": "ROBOT_COMING",
  "eta_sec": 18,
  "robot_id": "robot_01",
  "ts_ms": 1795400025200
}
```
- **`mode` hợp lệ:** `IDLE` (tắt/xanh nhạt), `QUEUED` (vàng nhấp nháy chậm), `ROBOT_COMING` (xanh dương thở), `ROBOT_ARRIVED` (xanh lá sáng), `ERROR` (đỏ nháy).

---

### 3.9. `dock/{dock_id}/status` (ESP32 Smart Dock → Broker, QoS 1, Retain=true, LWT)
```json
{
  "schema_version": 1,
  "dock_id": "dock_01",
  "online": true,
  "state": "CHARGING",
  "voltage_v": 14.40,
  "current_a": 2.80,
  "temp_c": 31.5,
  "ts_ms": 1795400030000
}
```
- **`state` hợp lệ:** `FREE`, `OCCUPIED`, `CHARGING`, `FAULT`.
