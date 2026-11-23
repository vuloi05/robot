"""Định nghĩa chuẩn các trạng thái FSM, loại tác vụ, độ ưu tiên và sự kiện khớp với docs/mqtt_protocol.md."""

from enum import Enum, IntEnum


class RobotState(str, Enum):
    """Trạng thái máy trạng thái tổng quát của robot (FSM)."""

    CHARGING = "CHARGING"
    IDLE = "IDLE"
    GO_KITCHEN = "GO_KITCHEN"
    LOADING_FOOD = "LOADING_FOOD"
    DELIVERING = "DELIVERING"
    WAITING_PICKUP = "WAITING_PICKUP"
    GO_RECEPTION = "GO_RECEPTION"
    GREETING_GUEST = "GREETING_GUEST"
    ESCORTING = "ESCORTING"
    ARRIVED_ESCORT = "ARRIVED_ESCORT"
    GO_TABLE_BUS = "GO_TABLE_BUS"
    LOADING_DISHES = "LOADING_DISHES"
    GO_DISHWASH = "GO_DISHWASH"
    DOCKING = "DOCKING"
    BLOCKED = "BLOCKED"
    ERROR = "ERROR"
    ESTOP = "ESTOP"


class TaskType(str, Enum):
    """Loại lệnh nghiệp vụ gửi qua MQTT robot/{id}/cmd."""

    DELIVERY = "DELIVERY"
    ESCORT = "ESCORT"
    BUSSING = "BUSSING"
    DOCK = "DOCK"
    UNDOCK = "UNDOCK"
    RETURN_HOME = "RETURN_HOME"
    CANCEL = "CANCEL"
    ESTOP = "ESTOP"
    CONFIRM_PICKUP = "CONFIRM_PICKUP"


class SpeedProfile(str, Enum):
    """Cấu hình giới hạn vận tốc/gia tốc tương ứng từng ngữ cảnh."""

    NORMAL = "NORMAL"
    ESCORT_SLOW = "ESCORT_SLOW"
    SMOOTH_LIQUID = "SMOOTH_LIQUID"


class TaskPriority(IntEnum):
    """Độ ưu tiên chuẩn cho hàng đợi điều phối nhiệm vụ."""

    CRITICAL_ESTOP = 100
    LOW_BATTERY = 90
    DELIVERY = 70
    ESCORT = 50
    BUSSING = 30
    IDLE_DOCK = 10


class EventType(str, Enum):
    """Loại sự kiện phát lên MQTT robot/{id}/event."""

    TASK_STARTED = "TASK_STARTED"
    ARRIVED_WAYPOINT = "ARRIVED_WAYPOINT"
    WAITING_PICKUP = "WAITING_PICKUP"
    PICKUP_CONFIRMED = "PICKUP_CONFIRMED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_FAILED = "TASK_FAILED"
    BLOCKED_WARNING = "BLOCKED_WARNING"
    BLOCKED_STUCK = "BLOCKED_STUCK"
    DOCKING_STARTED = "DOCKING_STARTED"
    DOCKED_CHARGING = "DOCKED_CHARGING"
    LOW_BATTERY = "LOW_BATTERY"
    ESTOP_TRIGGERED = "ESTOP_TRIGGERED"
