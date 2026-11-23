#!/usr/bin/env bash
# Script cài đặt môi trường phát triển cho Ubuntu 24.04 (Noble).
# Chạy bằng tài khoản thường (sẽ hỏi mật khẩu sudo ở các bước cài gói apt).

set -euo pipefail

usage() {
  cat <<'EOF'
Cách dùng: ./scripts/setup_dev_env.sh [TÙY CHỌN...]

Tùy chọn:
  --ros2       Cài ROS 2 Jazzy Desktop, Gazebo Harmonic, Nav2, SLAM, opennav_docking, apriltag_ros, colcon
  --docker     Cài Docker Engine + Docker Compose plugin + mosquitto-clients + python3-paho-mqtt
  --rust       Cài Rust toolchain (rustup + cargo) và sqlx-cli (SQLite)
  --node       Cài Node.js LTS thông qua nvm
  --embedded   Cài toolchain nhúng (gcc-arm-none-eabi, stlink-tools, openocd) & PlatformIO CLI
  --all        Cài toàn bộ các nhóm trên (--ros2 --docker --rust --node)
  --help, -h   Hiển thị trợ giúp này

Ví dụ:
  ./scripts/setup_dev_env.sh --ros2 --docker
  ./scripts/setup_dev_env.sh --all
EOF
}

if [[ $# -eq 0 ]]; then
  usage
  exit 0
fi

DO_ROS2=false
DO_DOCKER=false
DO_RUST=false
DO_NODE=false
DO_EMBEDDED=false

for arg in "$@"; do
  case "$arg" in
    --ros2) DO_ROS2=true ;;
    --docker) DO_DOCKER=true ;;
    --rust) DO_RUST=true ;;
    --node) DO_NODE=true ;;
    --embedded) DO_EMBEDDED=true ;;
    --all)
      DO_ROS2=true
      DO_DOCKER=true
      DO_RUST=true
      DO_NODE=true
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "[LỖI] Tham số không hợp lệ: $arg" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  source /etc/os-release
  if [[ "${UBUNTU_CODENAME:-}" != "noble" ]]; then
    echo "[CẢNH BÁO] Script tối ưu cho Ubuntu 24.04 (noble). Hệ thống hiện tại: ${PRETTY_NAME:-unknown}."
  fi
fi

install_ros2() {
  echo ">>> [1] Cài đặt ROS 2 Jazzy + Gazebo Harmonic + Nav2 Stack..."
  sudo apt-get update
  sudo apt-get install -y locales software-properties-common curl gnupg lsb-release
  sudo locale-gen en_US en_US.UTF-8
  sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

  sudo add-apt-repository -y universe
  sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg

  local codename
  codename="$(. /etc/os-release && echo "$UBUNTU_CODENAME")"
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu ${codename} main" | \
    sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

  sudo apt-get update
  sudo apt-get install -y \
    ros-jazzy-desktop \
    ros-dev-tools \
    python3-colcon-common-extensions \
    python3-rosdep \
    ros-jazzy-ros-gz \
    ros-jazzy-gz-ros2-control \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers \
    ros-jazzy-xacro \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-robot-localization \
    ros-jazzy-slam-toolbox \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup \
    ros-jazzy-opennav-docking \
    ros-jazzy-apriltag-ros \
    ros-jazzy-image-pipeline \
    ros-jazzy-teleop-twist-keyboard

  if [[ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]]; then
    sudo rosdep init || true
  fi
  rosdep update

  if ! grep -qF "source /opt/ros/jazzy/setup.bash" "$HOME/.bashrc"; then
    echo "source /opt/ros/jazzy/setup.bash" >> "$HOME/.bashrc"
  fi
  echo ">>> Hoàn tất ROS 2 Jazzy."
}

install_docker() {
  echo ">>> [2] Cài đặt Docker Engine + Compose + Mosquitto Clients..."
  sudo apt-get update
  sudo apt-get install -y ca-certificates curl mosquitto-clients python3-paho-mqtt python3-serial
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc

  local codename
  codename="$(. /etc/os-release && echo "$UBUNTU_CODENAME")"
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu ${codename} stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  sudo apt-get update
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  sudo usermod -aG docker "$USER" || true
  echo ">>> Hoàn tất Docker. Lưu ý: đăng xuất và đăng nhập lại để chạy docker không cần sudo."
}

install_rust() {
  echo ">>> [3] Cài đặt Rust (rustup + cargo + sqlx-cli)..."
  if ! command -v cargo >/dev/null 2>&1 && [[ ! -x "$HOME/.cargo/bin/cargo" ]]; then
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
  fi
  export PATH="$HOME/.cargo/bin:$PATH"
  if ! cargo install --list | grep -q "^sqlx-cli "; then
    cargo install sqlx-cli --no-default-features --features sqlite
  fi
  echo ">>> Hoàn tất Rust."
}

install_node() {
  echo ">>> [4] Cài đặt Node.js LTS qua nvm..."
  if [[ ! -d "$HOME/.nvm" ]]; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  fi
  export NVM_DIR="$HOME/.nvm"
  # shellcheck disable=SC1091
  source "$NVM_DIR/nvm.sh"
  nvm install --lts
  nvm alias default 'lts/*'
  echo ">>> Hoàn tất Node.js: $(node -v)"
}

install_embedded() {
  echo ">>> [5] Cài đặt công cụ nhúng STM32 & PlatformIO..."
  sudo apt-get update
  sudo apt-get install -y gcc-arm-none-eabi binutils-arm-none-eabi openocd stlink-tools pipx
  pipx ensurepath || true
  if ! command -v pio >/dev/null 2>&1; then
    pipx install platformio
  fi
  echo ">>> Hoàn tất công cụ nhúng."
}

$DO_ROS2 && install_ros2
$DO_DOCKER && install_docker
$DO_RUST && install_rust
$DO_NODE && install_node
$DO_EMBEDDED && install_embedded

echo ""
echo "Đã hoàn thành các bước cài đặt được chọn. Chạy './scripts/check_env.sh' để xác nhận lại."
