#ifndef RESTAURANT_ROBOT_SERIAL_PROTOCOL_H
#define RESTAURANT_ROBOT_SERIAL_PROTOCOL_H

#include <stddef.h>
#include <stdint.h>

#if defined(__cplusplus)
#define SP_STATIC_ASSERT(cond, msg) static_assert(cond, msg)
extern "C" {
#else
#define SP_STATIC_ASSERT(cond, msg) _Static_assert(cond, msg)
#endif

/* ============================================================================
 * Giao thức Serial nhị phân chuẩn (khớp 100% docs/serial_protocol.md)
 * Khung gói tin:
 *   SOF0(0xAA) | SOF1(0x55) | VER(0x01) | MSG_ID | SEQ | LEN | PAYLOAD | CRC16(LE)
 * ============================================================================ */

enum {
    SP_SOF0 = 0xAAu,
    SP_SOF1 = 0x55u,
    SP_PROTOCOL_VERSION = 0x01u,
    SP_MAX_PAYLOAD_LEN = 128u
};

/* Mã bản tin (MSG_ID) */
typedef enum {
    /* Pi 5 <-> STM32 (Tầng đáy: Motion, Power, Safety) */
    SP_MSG_CMD_WHEEL_VEL = 0x01u,
    SP_MSG_CMD_PID_CONFIG = 0x02u,
    SP_MSG_CMD_BASE_HEARTBEAT = 0x03u,
    SP_MSG_TEL_BASE_STATE = 0x11u,

    /* Pi 5 <-> ESP32 (Tầng trên: Tray, LED, ToF, Supervisor) */
    SP_MSG_CMD_TRAY_LED = 0x21u,
    SP_MSG_CMD_PI_HEARTBEAT = 0x22u,
    SP_MSG_TEL_UPPER_STATE = 0x31u
} sp_msg_id_t;

/* Bitmask lỗi cho TEL_BASE_STATE.fault_flags */
enum {
    SP_FAULT_ESTOP_HW = 1u << 0,
    SP_FAULT_WATCHDOG = 1u << 1,
    SP_FAULT_OVERCURRENT = 1u << 2,
    SP_FAULT_UNDERVOLTAGE = 1u << 3,
    SP_FAULT_IMU_ERR = 1u << 4
};

#pragma pack(push, 1)

typedef struct {
    uint8_t ver;
    uint8_t msg_id;
    uint8_t seq;
    uint8_t len;
} sp_frame_header_t;

/* 0x01: Pi 5 -> STM32 (10 bytes) */
typedef struct {
    float left_rad_s;
    float right_rad_s;
    uint8_t estop_req;
    uint8_t reserved;
} sp_cmd_wheel_vel_t;

/* 0x02: Pi 5 -> STM32 (16 bytes) */
typedef struct {
    float kp;
    float ki;
    float kd;
    uint16_t max_pwm;
    uint16_t reserved;
} sp_cmd_pid_config_t;

/* 0x03: Pi 5 -> STM32 (8 bytes) */
typedef struct {
    uint32_t pi_uptime_ms;
    uint8_t flags;
    uint8_t reserved[3];
} sp_cmd_base_heartbeat_t;

/* 0x11: STM32 -> Pi 5 (52 bytes) */
typedef struct {
    uint32_t mcu_time_ms;
    int32_t enc_left_ticks;
    int32_t enc_right_ticks;
    float vel_left_rad_s;
    float vel_right_rad_s;
    float imu_ax;
    float imu_ay;
    float imu_az;
    float imu_gx;
    float imu_gy;
    float imu_gz;
    uint16_t batt_mv;
    int16_t batt_ma;
    uint16_t fault_flags;
    uint16_t reserved;
} sp_tel_base_state_t;

/* 0x21: Pi 5 -> ESP32 tầng trên (12 bytes) */
typedef struct {
    uint8_t tray1_led_mode;
    uint8_t tray2_led_mode;
    uint8_t tray1_rgb[3];
    uint8_t tray2_rgb[3];
    uint8_t status_led_mode;
    uint8_t reserved[3];
} sp_cmd_tray_led_t;

/* 0x22: Pi 5 -> ESP32 tầng trên (8 bytes) */
typedef struct {
    uint32_t pi_uptime_ms;
    uint8_t fsm_state_code;
    uint8_t estop_req;
    uint8_t reserved[2];
} sp_cmd_pi_heartbeat_t;

/* 0x31: ESP32 tầng trên -> Pi 5 (18 bytes) */
typedef struct {
    uint32_t mcu_time_ms;
    uint8_t tray1_occupied;
    uint8_t tray2_occupied;
    int16_t tray1_weight_g;
    int16_t tray2_weight_g;
    uint16_t tof_front_mm;
    uint16_t tof_left_mm;
    uint16_t tof_right_mm;
    uint8_t button_flags;
    uint8_t fault_flags;
} sp_tel_upper_state_t;

#pragma pack(pop)

SP_STATIC_ASSERT(sizeof(sp_frame_header_t) == 4u, "sp_frame_header_t must be 4 bytes");
SP_STATIC_ASSERT(sizeof(sp_cmd_wheel_vel_t) == 10u, "sp_cmd_wheel_vel_t must be 10 bytes");
SP_STATIC_ASSERT(sizeof(sp_cmd_pid_config_t) == 16u, "sp_cmd_pid_config_t must be 16 bytes");
SP_STATIC_ASSERT(sizeof(sp_cmd_base_heartbeat_t) == 8u, "sp_cmd_base_heartbeat_t must be 8 bytes");
SP_STATIC_ASSERT(sizeof(sp_tel_base_state_t) == 52u, "sp_tel_base_state_t must be 52 bytes");
SP_STATIC_ASSERT(sizeof(sp_cmd_tray_led_t) == 12u, "sp_cmd_tray_led_t must be 12 bytes");
SP_STATIC_ASSERT(sizeof(sp_cmd_pi_heartbeat_t) == 8u, "sp_cmd_pi_heartbeat_t must be 8 bytes");
SP_STATIC_ASSERT(sizeof(sp_tel_upper_state_t) == 18u, "sp_tel_upper_state_t must be 18 bytes");

/**
 * Tính CRC16-CCITT (poly 0x1021, init 0xFFFF, xorout 0x0000).
 * Vùng tính: [VER, MSG_ID, SEQ, LEN, PAYLOAD...] (bỏ qua SOF0, SOF1).
 */
static inline uint16_t sp_crc16_ccitt(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFFu;
    for (size_t i = 0u; i < len; ++i) {
        crc ^= (uint16_t)((uint16_t)data[i] << 8u);
        for (uint8_t bit = 0u; bit < 8u; ++bit) {
            if ((crc & 0x8000u) != 0u) {
                crc = (uint16_t)((crc << 1u) ^ 0x1021u);
            } else {
                crc = (uint16_t)(crc << 1u);
            }
        }
    }
    return crc;
}

#if defined(__cplusplus)
}
#endif

#endif /* RESTAURANT_ROBOT_SERIAL_PROTOCOL_H */
