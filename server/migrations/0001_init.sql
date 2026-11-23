-- Lược đồ khởi tạo SQLite cho Restaurant Fleet Server (Contract v1)

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS waypoints (
    waypoint_id TEXT PRIMARY KEY,
    map_id      TEXT NOT NULL DEFAULT 'restaurant_floor_1',
    kind        TEXT NOT NULL CHECK (kind IN ('TABLE', 'KITCHEN_PICKUP', 'KITCHEN_DISHWASH', 'RECEPTION', 'DOCK', 'PRE_DOCK')),
    label       TEXT NOT NULL,
    x           REAL NOT NULL,
    y           REAL NOT NULL,
    yaw         REAL NOT NULL DEFAULT 0.0,
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tables (
    table_id    TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    waypoint_id TEXT NOT NULL REFERENCES waypoints(waypoint_id) ON UPDATE CASCADE,
    status      TEXT NOT NULL DEFAULT 'AVAILABLE' CHECK (status IN ('AVAILABLE', 'OCCUPIED', 'NEEDS_BUSSING', 'RESERVED')),
    led_mode    TEXT NOT NULL DEFAULT 'IDLE',
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS robots (
    robot_id        TEXT PRIMARY KEY,
    online          INTEGER NOT NULL DEFAULT 0,
    mode            TEXT NOT NULL DEFAULT 'sim',
    fsm_state       TEXT NOT NULL DEFAULT 'IDLE',
    battery_pct     REAL NOT NULL DEFAULT 100.0,
    is_charging     INTEGER NOT NULL DEFAULT 0,
    current_map_id  TEXT NOT NULL DEFAULT 'restaurant_floor_1',
    pose_x          REAL NOT NULL DEFAULT 0.0,
    pose_y          REAL NOT NULL DEFAULT 0.0,
    pose_yaw        REAL NOT NULL DEFAULT 0.0,
    last_seen_ms    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tasks (
    task_id         TEXT PRIMARY KEY,
    cmd_id          TEXT NOT NULL UNIQUE,
    robot_id        TEXT REFERENCES robots(robot_id),
    task_type       TEXT NOT NULL CHECK (task_type IN ('DELIVERY', 'ESCORT', 'BUSSING', 'DOCK', 'UNDOCK', 'RETURN_HOME', 'CANCEL', 'ESTOP')),
    priority        INTEGER NOT NULL,
    speed_profile   TEXT NOT NULL DEFAULT 'NORMAL',
    status          TEXT NOT NULL DEFAULT 'QUEUED' CHECK (status IN ('QUEUED', 'DISPATCHED', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED')),
    source_role     TEXT NOT NULL DEFAULT 'kitchen',
    created_at_ms   INTEGER NOT NULL,
    updated_at_ms   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS task_stops (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id         TEXT NOT NULL REFERENCES tasks(task_id) ON DELETE CASCADE,
    stop_index      INTEGER NOT NULL,
    waypoint_id     TEXT NOT NULL REFERENCES waypoints(waypoint_id),
    tray_ids_json   TEXT NOT NULL DEFAULT '[]',
    voice_message   TEXT NOT NULL DEFAULT '',
    wait_timeout_sec INTEGER NOT NULL DEFAULT 120,
    arrived_at_ms   INTEGER,
    completed_at_ms INTEGER,
    UNIQUE(task_id, stop_index)
);

CREATE TABLE IF NOT EXISTS telemetry_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    robot_id        TEXT NOT NULL,
    fsm_state       TEXT NOT NULL,
    pose_x          REAL NOT NULL,
    pose_y          REAL NOT NULL,
    pose_yaw        REAL NOT NULL,
    battery_pct     REAL NOT NULL,
    ts_ms           INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_tasks_status_priority ON tasks(status, priority DESC, created_at_ms ASC);
CREATE INDEX IF NOT EXISTS idx_telemetry_robot_ts ON telemetry_logs(robot_id, ts_ms DESC);
