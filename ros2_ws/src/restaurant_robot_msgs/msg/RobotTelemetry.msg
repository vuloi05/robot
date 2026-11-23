# Telemetry tổng hợp xuất bản từ mission_manager cho restaurant_mqtt_bridge
std_msgs/Header header

string robot_id
string map_id
float64 x
float64 y
float64 yaw
float64 linear_vx
float64 angular_omega

float32 battery_voltage_v
float32 battery_current_a
float32 battery_pct
bool is_charging

string fsm_state
string active_task_id
string current_target

TrayState[] trays

bool estop
bool obstacle_blocked
uint16 tof_front_mm
