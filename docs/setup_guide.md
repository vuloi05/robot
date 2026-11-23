# Hướng Dẫn Cài Đặt Môi Trường Phát Triển (Ubuntu 24.04 LTS)

Tài liệu hướng dẫn cài đặt đầy đủ công cụ trên máy **Ubuntu 24.04 LTS (Noble Numbat)** phục vụ toàn bộ 6 giai đoạn phát triển.

> [!TIP]
> Có thể chạy nhanh script tự động trong [setup_dev_env.sh](../scripts/setup_dev_env.sh) hoặc tự chạy từng bước thủ công bên dưới. Sau khi cài, luôn kiểm tra lại bằng `./scripts/check_env.sh`.

---

## 0. Kiểm Tra Hiện Trạng Máy

```bash
./scripts/check_env.sh
```

---

## 1. Cài Đặt ROS 2 Jazzy + Gazebo Harmonic + Nav2 Stack

### 1.1. Thêm repository chính thức của ROS 2
```bash
sudo apt update && sudo apt install -y locales software-properties-common curl gnupg lsb-release
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

sudo add-apt-repository -y universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo "$UBUNTU_CODENAME") main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### 1.2. Cài ROS 2 Jazzy Desktop, Gazebo Harmonic, Nav2, Auto-Docking & Tools
```bash
sudo apt update
sudo apt install -y \
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
```

### 1.3. Khởi tạo `rosdep` & thêm vào `~/.bashrc`
```bash
sudo rosdep init 2>/dev/null || true
rosdep update
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 1.4. Lưu ý GPU Hybrid (Intel + NVIDIA RTX 3050 trên Laptop) khi chạy Gazebo Harmonic
Nếu chạy `gz sim` bị tụt FPS hoặc lỗi render OpenGL trên laptop có GPU kép (Intel Iris Xe + NVIDIA RTX 3050), hãy dùng biến offload NVIDIA khi khởi chạy Gazebo:
```bash
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia gz sim
```

---

## 2. Cài Đặt Docker Engine & Mosquitto Clients

### 2.1. Docker Engine (Ubuntu 24.04)
```bash
sudo apt update && sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$UBUNTU_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"
# Đăng xuất và đăng nhập lại để nhóm docker có hiệu lực
```

### 2.2. Công cụ test MQTT (`mosquitto-clients`)
```bash
sudo apt install -y mosquitto-clients
```
Thư viện Python cho node `restaurant_mqtt_bridge`:
```bash
pip3 install --user --break-system-packages paho-mqtt pyserial
```
*(Khuyên dùng `paho-mqtt` qua `apt` nếu có: `sudo apt install -y python3-paho-mqtt python3-serial` để tránh xung đột với Python hệ thống).*

---

## 3. Cài Đặt Rust Toolchain (Cho `server/`)

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
cargo install sqlx-cli --no-default-features --features sqlite
```

---

## 4. Cài Đặt Node.js 22 LTS (Cho `web_app/`)

Khuyên dùng **nvm** (hoặc NodeSource) để cài Node 22 LTS sạch sẽ:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source "$HOME/.nvm/nvm.sh"
nvm install --lts
node -v && npm -v
```

---

## 5. Công Cụ Nhúng Cho Giai Đoạn 4–5 (STM32 & ESP32)

- **ESP32 (`firmware_robot_esp32/`, `firmware_iot/`):** Cài **PlatformIO CLI** hoặc Extension PlatformIO trên VS Code (`pipx install platformio` hoặc thông qua VS Code).
- **STM32 (`firmware_robot_stm32/`):** Cài **STM32CubeIDE** hoặc **STM32CubeCLT + CMake + `arm-none-eabi-gcc`**:
  ```bash
  sudo apt install -y gcc-arm-none-eabi binutils-arm-none-eabi openocd stlink-tools
  ```
