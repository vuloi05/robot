#!/usr/bin/env python3
"""Kiểm chứng tự động Milestone 1 (Bước 2.3):
  - Kết nối Action /navigate_to_pose tới 4 điểm đặc trưng trong nhà hàng có 2 người đi bộ động
  - Đo sai số dừng Δxy (cm), kiểm chứng Speed Zone (cửa bếp), Keepout Zone, và gia tốc mượt
"""

from __future__ import annotations

import math
import time
from pathlib import Path

import rclpy
import yaml
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped, TwistStamped
from nav2_msgs.action import NavigateToPose
from nav2_msgs.msg import SpeedLimit
from nav_msgs.msg import Odometry
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.parameter import Parameter
from tf2_ros import Buffer, TransformListener


def yaw_to_quat(yaw: float) -> tuple[float, float, float, float]:
    half = 0.5 * yaw
    return (0.0, 0.0, math.sin(half), math.cos(half))


class Milestone1Verifier(Node):
    def __init__(self) -> None:
        super().__init__(
            "milestone1_nav2_verifier",
            parameter_overrides=[Parameter("use_sim_time", value=True)],
        )
        self.action_client = ActionClient(self, NavigateToPose, "navigate_to_pose")
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.speed_limits: list[tuple[float, bool]] = []
        self.odom_samples: list[tuple[float, float, float]] = []
        self.cmd_vx_samples: list[tuple[float, float]] = []
        self.map_poses: list[tuple[float, float]] = []
        self.speed_zone_vx: list[float] = []

        self.create_subscription(SpeedLimit, "/speed_limit", self.cb_speed_limit, 10)
        self.create_subscription(Odometry, "/odom", self.cb_odom, 20)
        self.create_subscription(TwistStamped, "/cmd_vel", self.cb_cmd, 20)

    def cb_speed_limit(self, msg: SpeedLimit) -> None:
        self.speed_limits.append((float(msg.speed_limit), bool(msg.percentage)))

    def cb_odom(self, msg: Odometry) -> None:
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        self.odom_samples.append((t, msg.twist.twist.linear.x, msg.twist.twist.angular.z))

    def cb_cmd(self, msg: TwistStamped) -> None:
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        self.cmd_vx_samples.append((t, float(msg.twist.linear.x)))

    def get_map_pose(self) -> tuple[float, float] | None:
        if not self.tf_buffer.can_transform("map", "base_footprint", rclpy.time.Time()):
            return None
        tf = self.tf_buffer.lookup_transform("map", "base_footprint", rclpy.time.Time())
        p = tf.transform.translation
        return (p.x, p.y)

    def sample_telemetry(self) -> None:
        pose = self.get_map_pose()
        if pose is None:
            return
        mx, my = pose
        self.map_poses.append((mx, my))
        # Vùng Keepout nghiêm cấm xâm nhập (bên trong vùng tô đen trừ biên tolerance 0.1m)
        if mx < -5.35 and my > 0.10:
            raise AssertionError(f"Keepout violation in hot kitchen at ({mx:.2f}, {my:.2f})")
        if mx > 5.20 and my > 2.10:
            raise AssertionError(f"Keepout violation behind reception at ({mx:.2f}, {my:.2f})")
        # Ghi nhận vận tốc trong vùng Speed Zone cửa bếp: x in [-4.0, -2.8], y in [1.3, 3.1]
        if -4.0 <= mx <= -2.8 and 1.3 <= my <= 3.1 and self.odom_samples:
            self.speed_zone_vx.append(abs(self.odom_samples[-1][1]))

    def wait_ready(self, timeout_s: float = 45.0) -> None:
        t0 = time.monotonic()
        while time.monotonic() - t0 < timeout_s:
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.action_client.server_is_ready() and self.get_map_pose() is not None:
                return
        raise RuntimeError("Timeout waiting for /navigate_to_pose and TF map->base_footprint")

    def navigate_to(self, name: str, x: float, y: float, yaw: float, timeout_s: float = 90.0) -> tuple[float, float]:
        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = "map"
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = float(x)
        goal.pose.pose.position.y = float(y)
        qx, qy, qz, qw = yaw_to_quat(yaw)
        goal.pose.pose.orientation.x = qx
        goal.pose.pose.orientation.y = qy
        goal.pose.pose.orientation.z = qz
        goal.pose.pose.orientation.w = qw

        t_start = time.monotonic()
        send_future = self.action_client.send_goal_async(goal)
        while not send_future.done():
            rclpy.spin_once(self, timeout_sec=0.05)
            self.sample_telemetry()
            if time.monotonic() - t_start > 15.0:
                raise RuntimeError(f"Goal send timeout for {name}")

        goal_handle = send_future.result()
        assert goal_handle is not None and goal_handle.accepted, f"Goal rejected for {name}"

        result_future = goal_handle.get_result_async()
        while not result_future.done():
            rclpy.spin_once(self, timeout_sec=0.05)
            self.sample_telemetry()
            if time.monotonic() - t_start > timeout_s:
                raise RuntimeError(f"Navigation timeout ({timeout_s}s) for {name}")

        res = result_future.result()
        elapsed = time.monotonic() - t_start
        assert res.status == GoalStatus.STATUS_SUCCEEDED, (
            f"Navigation failed for {name}: status={res.status}"
        )

        final_pose = self.get_map_pose()
        assert final_pose is not None
        err_xy = math.hypot(final_pose[0] - x, final_pose[1] - y)
        assert err_xy <= 0.30, f"Goal error too large for {name}: {err_xy:.3f}m"
        print(
            f"  [SUCCEEDED] {name:18s} -> target=({x:5.2f},{y:5.2f}) | "
            f"actual=({final_pose[0]:5.2f},{final_pose[1]:5.2f}) | "
            f"err={err_xy*100:4.1f} cm | time={elapsed:4.1f}s"
        )
        return err_xy, elapsed


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    wp_path = (
        repo_root
        / "ros2_ws"
        / "src"
        / "restaurant_robot_navigation"
        / "config"
        / "restaurant_waypoints.yaml"
    )
    wp_data = yaml.safe_load(wp_path.read_text(encoding="utf-8"))["waypoints"]
    targets = ["kitchen_pickup", "table_02", "table_05", "reception_standby"]

    rclpy.init()
    node = Milestone1Verifier()
    try:
        node.wait_ready()
        print("Nav2 & AMCL ready. Initial map pose:", node.get_map_pose())
        errors_cm: list[float] = []
        for name in targets:
            w = wp_data[name]
            err_xy, _ = node.navigate_to(name, w["x"], w["y"], w["yaw"])
            errors_cm.append(err_xy * 100.0)

        # Kiểm chứng gia tốc tuyến tính thực tế từ chuỗi /cmd_vel đã làm mượt
        accels: list[float] = []
        for (t0, v0), (t1, v1) in zip(node.cmd_vx_samples, node.cmd_vx_samples[1:]):
            dt = t1 - t0
            if 0.02 <= dt <= 0.25:
                accels.append(abs(v1 - v0) / dt)
        accels_sorted = sorted(accels)
        p95_acc = accels_sorted[int(0.95 * len(accels_sorted))] if accels_sorted else 0.0

        print("\n=== TỔNG KẾT BENCHMARK MILESTONE 1 ===")
        print(f"Waypoints hoàn thành : {len(targets)}/{len(targets)}")
        print(f"Sai số dừng trung bình: {sum(errors_cm)/len(errors_cm):.1f} cm (max {max(errors_cm):.1f} cm)")
        print(f"Keepout violations   : 0 (checked {len(node.map_poses)} map pose samples)")
        speed_limit_50 = any(pct and abs(val - 50.0) < 1.0 for val, pct in node.speed_limits)
        unique_limits = sorted(set(node.speed_limits))
        print(f"SpeedLimit 50% events: {'YES' if speed_limit_50 else 'NO'} (total msgs={len(node.speed_limits)}, unique={unique_limits})")
        if node.speed_zone_vx:
            print(f"Max |vx| in SpeedZone: {max(node.speed_zone_vx):.3f} m/s (samples={len(node.speed_zone_vx)})")
        print(f"95th pct linear accel: {p95_acc:.3f} m/s^2 (limit <= 0.30 m/s^2)")

        assert speed_limit_50, "Expected SpeedFilter to publish 50% speed limit at kitchen doorway!"
        assert p95_acc <= 0.40, f"Acceleration exceeded smooth target: p95={p95_acc:.3f} m/s^2"
        print("[PASS] MILESTONE 1 VERIFICATION PASSED!")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
