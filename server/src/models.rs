//! Mô hình dữ liệu chuẩn khớp 1-1 với `docs/mqtt_protocol.md` (Contract v1) và `web_app/src/types/protocol.ts`.

#![allow(dead_code)]

use serde::{Deserialize, Serialize};

pub const SCHEMA_VERSION: u32 = 1;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum RobotState {
    Charging,
    Idle,
    GoKitchen,
    LoadingFood,
    Delivering,
    WaitingPickup,
    GoReception,
    GreetingGuest,
    Escorting,
    ArrivedEscort,
    GoTableBus,
    LoadingDishes,
    GoDishwash,
    Docking,
    Blocked,
    Error,
    Estop,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum TaskType {
    Delivery,
    Escort,
    Bussing,
    Dock,
    Undock,
    ReturnHome,
    Cancel,
    Estop,
    ConfirmPickup,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum SpeedProfile {
    Normal,
    EscortSlow,
    SmoothLiquid,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum EventType {
    TaskStarted,
    ArrivedWaypoint,
    WaitingPickup,
    PickupConfirmed,
    TaskCompleted,
    TaskFailed,
    BlockedWarning,
    BlockedStuck,
    DockingStarted,
    DockedCharging,
    LowBattery,
    EstopTriggered,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum TableCallAction {
    Bussing,
    CallStaff,
    Cancel,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum TableCallSource {
    Esp32Button,
    QrWeb,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum TableLedMode {
    Idle,
    Queued,
    RobotComing,
    RobotArrived,
    Error,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum DockState {
    Free,
    Occupied,
    Charging,
    Fault,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Pose2D {
    pub map_id: String,
    pub x: f64,
    pub y: f64,
    pub yaw: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Velocity2D {
    pub vx: f64,
    pub omega: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BatteryInfo {
    pub voltage_v: f32,
    pub current_a: f32,
    pub pct: f32,
    pub is_charging: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrayState {
    pub tray_id: u8,
    pub occupied: bool,
    pub weight_g: i32,
    pub assigned_table: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SafetyState {
    pub estop: bool,
    pub obstacle_blocked: bool,
    pub tof_front_mm: u16,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RobotStatus {
    pub schema_version: u32,
    pub robot_id: String,
    pub online: bool,
    pub mode: String,
    pub firmware_version: String,
    pub ts_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RobotTelemetry {
    pub schema_version: u32,
    pub robot_id: String,
    pub pose: Pose2D,
    pub velocity: Velocity2D,
    pub battery: BatteryInfo,
    pub fsm_state: RobotState,
    pub active_task_id: Option<String>,
    pub current_target: Option<String>,
    pub trays: Vec<TrayState>,
    pub safety: SafetyState,
    pub ts_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MissionStop {
    pub stop_index: u16,
    pub waypoint_id: String,
    pub tray_ids: Vec<u8>,
    pub voice_message: String,
    pub wait_timeout_sec: u16,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RobotCommand {
    pub schema_version: u32,
    pub cmd_id: String,
    pub task_id: String,
    #[serde(rename = "type")]
    pub task_type: TaskType,
    pub priority: u8,
    pub speed_profile: SpeedProfile,
    pub stops: Vec<MissionStop>,
    pub ts_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RobotCommandAck {
    pub schema_version: u32,
    pub robot_id: String,
    pub cmd_id: String,
    pub task_id: String,
    pub accepted: bool,
    pub reason: String,
    pub ts_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RobotEvent {
    pub schema_version: u32,
    pub robot_id: String,
    pub task_id: Option<String>,
    pub event_type: EventType,
    pub waypoint_id: Option<String>,
    pub tray_ids: Vec<u8>,
    pub message: String,
    pub ts_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SupervisorReport {
    pub schema_version: u32,
    pub robot_id: String,
    pub online: bool,
    pub pi_alive: bool,
    pub battery_voltage_v: f32,
    pub battery_pct: f32,
    pub trays: Vec<TrayState>,
    pub estop: bool,
    pub ts_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TableCall {
    pub schema_version: u32,
    pub call_id: String,
    pub table_id: String,
    pub action: TableCallAction,
    pub source: TableCallSource,
    pub ts_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TableLedCommand {
    pub schema_version: u32,
    pub table_id: String,
    pub mode: TableLedMode,
    pub eta_sec: Option<u32>,
    pub robot_id: Option<String>,
    pub ts_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DockStatus {
    pub schema_version: u32,
    pub dock_id: String,
    pub online: bool,
    pub state: DockState,
    pub voltage_v: f32,
    pub current_a: f32,
    pub temp_c: f32,
    pub ts_ms: u64,
}
