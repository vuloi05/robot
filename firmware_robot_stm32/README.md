# Firmware STM32 Tầng Đáy Robot (Motion, Power & Safety Core)

MCU tầng đáy (**STM32F407VET6 / STM32F103C8T6**) đảm nhiệm toàn bộ tác vụ **thời gian thực cứng (Hard Real-time)** theo kiến trúc Cách B.

## Phân Bổ Ngoại Vi Khuyến Nghị

| Chức năng | Ngoại vi STM32 | Ghi chú kỹ thuật |
| :--- | :--- | :--- |
| **Encoder bánh Trái / Phải** | Hardware Timer Encoder Mode (`TIM2`, `TIM3`) | Đếm xung Quadrature bằng phần cứng 32-bit/16-bit, không rớt xung |
| **Điều khiển Driver Motor (BTS7960 / MDD10A)** | PWM Timer (`TIM1` / `TIM4`) + GPIO DIR | Tần số PWM 20 kHz (êm tai, không rít), vòng lặp PID 50–100 Hz |
| **IMU (BNO055 / MPU6050 / WT901)** | `I2C1` (hoặc `USART2`) | Gửi cùng gói `TEL_BASE_STATE` (`0x11`) về Pi 5 |
| **Đo áp & dòng Pin (INA219/INA226)** | `I2C1` | Báo `batt_mv` và `batt_ma` (phát hiện đang sạc khi vào dock) |
| **Nút E-Stop cứng** | `EXTI` ngắt ngoài + Relay cắt nguồn motor | Kéo cờ `FAULT_ESTOP_HW` ngay lập tức |
| **Giao tiếp Pi 5 (`/dev/robot_stm32`)** | `USART1` + DMA / USB CDC (`230400 bps`) | Giao thức nhị phân CRC16 trong [serial_protocol.h](include/serial_protocol.h) |
| **An toàn Watchdog** | Software/IWDG Timer `500 ms` | Mất frame hợp lệ từ Pi 5 quá 500 ms → phanh dừng & bật `FAULT_WATCHDOG` |

> Triển khai code đầy đủ ở **Giai đoạn 5**.
