"""Hằng số và hàm tạo tên topic MQTT chuẩn khớp 100% docs/mqtt_protocol.md (Contract v1)."""

SCHEMA_VERSION: int = 1


def robot_status_topic(robot_id: str) -> str:
    """Topic online/offline (QoS 1, Retain=true, LWT)."""
    return f"robot/{robot_id}/status"


def robot_telemetry_topic(robot_id: str) -> str:
    """Topic telemetry 2-5 Hz (QoS 0)."""
    return f"robot/{robot_id}/telemetry"


def robot_cmd_topic(robot_id: str) -> str:
    """Topic nhận lệnh điều khiển từ Server (QoS 1)."""
    return f"robot/{robot_id}/cmd"


def robot_cmd_ack_topic(robot_id: str) -> str:
    """Topic xác nhận nhận lệnh về Server (QoS 1)."""
    return f"robot/{robot_id}/cmd_ack"


def robot_event_topic(robot_id: str) -> str:
    """Topic phát sự kiện nhiệm vụ/cảnh báo lên Server (QoS 1)."""
    return f"robot/{robot_id}/event"


def robot_supervisor_topic(robot_id: str) -> str:
    """Topic giám sát out-of-band từ ESP32 tầng trên (QoS 1, Retain=true, LWT)."""
    return f"robot/{robot_id}/supervisor"


def table_call_topic(table_id: str) -> str:
    """Topic gọi/hủy từ nút ESP32 tại bàn hoặc QR web (QoS 1)."""
    return f"table/{table_id}/call"


def table_led_topic(table_id: str) -> str:
    """Topic cập nhật LED phản hồi tới nút gọi bàn (QoS 1, Retain=true)."""
    return f"table/{table_id}/led"


def dock_status_topic(dock_id: str) -> str:
    """Topic trạng thái trạm sạc thông minh (QoS 1, Retain=true, LWT)."""
    return f"dock/{dock_id}/status"
