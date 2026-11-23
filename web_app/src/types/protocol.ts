// Định nghĩa kiểu dữ liệu chuẩn khớp 1-1 với docs/mqtt_protocol.md (Contract v1) và server/src/models.rs

export const SCHEMA_VERSION = 1 as const;

export type RobotState =
  | "CHARGING"
  | "IDLE"
  | "GO_KITCHEN"
  | "LOADING_FOOD"
  | "DELIVERING"
  | "WAITING_PICKUP"
  | "GO_RECEPTION"
  | "GREETING_GUEST"
  | "ESCORTING"
  | "ARRIVED_ESCORT"
  | "GO_TABLE_BUS"
  | "LOADING_DISHES"
  | "GO_DISHWASH"
  | "DOCKING"
  | "BLOCKED"
  | "ERROR"
  | "ESTOP";

export type TaskType =
  | "DELIVERY"
  | "ESCORT"
  | "BUSSING"
  | "DOCK"
  | "UNDOCK"
  | "RETURN_HOME"
  | "CANCEL"
  | "ESTOP"
  | "CONFIRM_PICKUP";

export type SpeedProfile = "NORMAL" | "ESCORT_SLOW" | "SMOOTH_LIQUID";

export type EventType =
  | "TASK_STARTED"
  | "ARRIVED_WAYPOINT"
  | "WAITING_PICKUP"
  | "PICKUP_CONFIRMED"
  | "TASK_COMPLETED"
  | "TASK_FAILED"
  | "BLOCKED_WARNING"
  | "BLOCKED_STUCK"
  | "DOCKING_STARTED"
  | "DOCKED_CHARGING"
  | "LOW_BATTERY"
  | "ESTOP_TRIGGERED";

export type TableCallAction = "BUSSING" | "CALL_STAFF" | "CANCEL";
export type TableCallSource = "esp32_button" | "qr_web";
export type TableLedMode =
  | "IDLE"
  | "QUEUED"
  | "ROBOT_COMING"
  | "ROBOT_ARRIVED"
  | "ERROR";
export type DockState = "FREE" | "OCCUPIED" | "CHARGING" | "FAULT";

export interface Pose2D {
  map_id: string;
  x: number;
  y: number;
  yaw: number;
}

export interface Velocity2D {
  vx: number;
  omega: number;
}

export interface BatteryInfo {
  voltage_v: number;
  current_a: number;
  pct: number;
  is_charging: boolean;
}

export interface TrayState {
  tray_id: number;
  occupied: boolean;
  weight_g: number;
  assigned_table: string | null;
}

export interface SafetyState {
  estop: boolean;
  obstacle_blocked: boolean;
  tof_front_mm: number;
}

export interface RobotStatus {
  schema_version: number;
  robot_id: string;
  online: boolean;
  mode: string;
  firmware_version: string;
  ts_ms: number;
}

export interface RobotTelemetry {
  schema_version: number;
  robot_id: string;
  pose: Pose2D;
  velocity: Velocity2D;
  battery: BatteryInfo;
  fsm_state: RobotState;
  active_task_id: string | null;
  current_target: string | null;
  trays: TrayState[];
  safety: SafetyState;
  ts_ms: number;
}

export interface MissionStop {
  stop_index: number;
  waypoint_id: string;
  tray_ids: number[];
  voice_message: string;
  wait_timeout_sec: number;
}

export interface RobotCommand {
  schema_version: number;
  cmd_id: string;
  task_id: string;
  type: TaskType;
  priority: number;
  speed_profile: SpeedProfile;
  stops: MissionStop[];
  ts_ms: number;
}

export interface RobotCommandAck {
  schema_version: number;
  robot_id: string;
  cmd_id: string;
  task_id: string;
  accepted: boolean;
  reason: string;
  ts_ms: number;
}

export interface RobotEvent {
  schema_version: number;
  robot_id: string;
  task_id: string | null;
  event_type: EventType;
  waypoint_id: string | null;
  tray_ids: number[];
  message: string;
  ts_ms: number;
}

export interface SupervisorReport {
  schema_version: number;
  robot_id: string;
  online: boolean;
  pi_alive: boolean;
  battery_voltage_v: number;
  battery_pct: number;
  trays: TrayState[];
  estop: boolean;
  ts_ms: number;
}

export interface TableCall {
  schema_version: number;
  call_id: string;
  table_id: string;
  action: TableCallAction;
  source: TableCallSource;
  ts_ms: number;
}

export interface TableLedCommand {
  schema_version: number;
  table_id: string;
  mode: TableLedMode;
  eta_sec: number | null;
  robot_id: string | null;
  ts_ms: number;
}

export interface DockStatus {
  schema_version: number;
  dock_id: string;
  online: boolean;
  state: DockState;
  voltage_v: number;
  current_a: number;
  temp_c: number;
  ts_ms: number;
}
