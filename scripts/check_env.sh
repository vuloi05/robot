#!/usr/bin/env bash
# Kiểm tra read-only các công cụ phát triển cho dự án Robot Nhà Hàng.
# Luôn thoát với mã 0 để dễ tổng hợp trạng thái.

set -u

export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"
set +u
if [[ -s "$HOME/.nvm/nvm.sh" ]]; then
  # shellcheck disable=SC1091
  source "$HOME/.nvm/nvm.sh" >/dev/null 2>&1 || true
fi
if [[ -f /opt/ros/jazzy/setup.bash ]]; then
  # shellcheck disable=SC1091
  source /opt/ros/jazzy/setup.bash >/dev/null 2>&1 || true
fi
set -u

ok_count=0
miss_count=0

print_ok() {
  local label="$1"
  local detail="$2"
  printf "  [OK]      %-24s %s\n" "$label" "$detail"
  ok_count=$((ok_count + 1))
}

print_missing() {
  local label="$1"
  local hint="$2"
  printf "  [MISSING] %-24s -> %s\n" "$label" "$hint"
  miss_count=$((miss_count + 1))
}

check_cmd() {
  local label="$1"
  local cmd="$2"
  local ver_flag="$3"
  local hint="$4"
  if command -v "$cmd" >/dev/null 2>&1; then
    local ver
    local -a flags=()
    read -ra flags <<< "$ver_flag"
    ver="$("$cmd" "${flags[@]}" 2>&1 | head -n 1 || true)"
    print_ok "$label" "$ver"
  else
    print_missing "$label" "$hint"
  fi
}

check_ros_pkg_dir() {
  local label="$1"
  local pkg_dir="$2"
  local hint="$3"
  if [[ -d "/opt/ros/jazzy/share/$pkg_dir" ]]; then
    print_ok "$label" "/opt/ros/jazzy/share/$pkg_dir"
  else
    print_missing "$label" "$hint"
  fi
}

echo "=================================================================="
echo "  Kiểm Tra Môi Trường Phát Triển - Robot Phục Vụ Nhà Hàng"
echo "=================================================================="
if [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  source /etc/os-release
  echo "Hệ điều hành : ${PRETTY_NAME:-Unknown} (${UBUNTU_CODENAME:-unknown})"
fi
echo "Kiến trúc    : $(uname -m) | Kernel: $(uname -r)"
echo ""

echo "[1/5] Công cụ hệ thống cơ bản:"
check_cmd "git" "git" "--version" "sudo apt install -y git"
check_cmd "python3" "python3" "--version" "sudo apt install -y python3"
check_cmd "pip3" "pip3" "--version" "sudo apt install -y python3-pip"
check_cmd "cmake" "cmake" "--version" "sudo apt install -y cmake"
check_cmd "g++" "g++" "--version" "sudo apt install -y g++"
echo ""

echo "[2/5] ROS 2 Jazzy & Gazebo Harmonic (Tầng 1, 3, 4):"
if [[ -f /opt/ros/jazzy/setup.bash ]]; then
  print_ok "ROS 2 Jazzy" "/opt/ros/jazzy/setup.bash"
elif command -v ros2 >/dev/null 2>&1; then
  print_ok "ros2 CLI" "$(command -v ros2)"
else
  print_missing "ROS 2 Jazzy" "./scripts/setup_dev_env.sh --ros2"
fi
check_cmd "gz (Gazebo)" "gz" "sim --version" "./scripts/setup_dev_env.sh --ros2"
check_cmd "colcon" "colcon" "--version" "sudo apt install -y python3-colcon-common-extensions"
check_ros_pkg_dir "nav2_bringup" "nav2_bringup" "sudo apt install -y ros-jazzy-nav2-bringup"
check_ros_pkg_dir "slam_toolbox" "slam_toolbox" "sudo apt install -y ros-jazzy-slam-toolbox"
check_ros_pkg_dir "opennav_docking" "opennav_docking" "sudo apt install -y ros-jazzy-opennav-docking"
check_ros_pkg_dir "robot_localization" "robot_localization" "sudo apt install -y ros-jazzy-robot-localization"
check_ros_pkg_dir "apriltag_ros" "apriltag_ros" "sudo apt install -y ros-jazzy-apriltag-ros"
check_ros_pkg_dir "gz_ros2_control" "gz_ros2_control" "sudo apt install -y ros-jazzy-gz-ros2-control"
echo ""

echo "[3/5] Hạ tầng MQTT & Container (Tầng 5):"
check_cmd "docker" "docker" "--version" "./scripts/setup_dev_env.sh --docker"
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  print_ok "docker compose" "$(docker compose version 2>&1 | head -n 1)"
else
  print_missing "docker compose" "./scripts/setup_dev_env.sh --docker"
fi
check_cmd "mosquitto_pub" "mosquitto_pub" "--help" "sudo apt install -y mosquitto-clients"
echo ""

echo "[4/5] Backend Rust & Frontend React (Tầng 5, 6):"
check_cmd "rustc" "rustc" "--version" "./scripts/setup_dev_env.sh --rust"
check_cmd "cargo" "cargo" "--version" "./scripts/setup_dev_env.sh --rust"
check_cmd "node" "node" "--version" "./scripts/setup_dev_env.sh --node"
check_cmd "npm" "npm" "--version" "./scripts/setup_dev_env.sh --node"
echo ""

echo "[5/5] Công cụ nhúng (Tầng 2 - cho GĐ 4-5):"
check_cmd "arm-none-eabi-gcc" "arm-none-eabi-gcc" "--version" "./scripts/setup_dev_env.sh --embedded"
check_cmd "pio (PlatformIO)" "pio" "--version" "./scripts/setup_dev_env.sh --embedded"
echo ""

echo "=================================================================="
echo "  Tổng kết: $ok_count đã sẵn sàng | $miss_count chưa cài"
echo "  Xem hướng dẫn chi tiết tại: docs/setup_guide.md"
echo "=================================================================="
exit 0
