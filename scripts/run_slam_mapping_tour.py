#!/usr/bin/env python3
"""Tự động lái robot đi vòng kín quanh nhà hàng tĩnh để quét bản đồ SLAM
và lưu thành restaurant_floor_1.{yaml,pgm} + đo sai số kích thước phòng.
"""

from __future__ import annotations

import math
import subprocess
import time
from pathlib import Path

import rclpy
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import OccupancyGrid, Odometry
from PIL import Image
from rclpy.node import Node
from rclpy.parameter import Parameter


def quat_to_yaw(q) -> float:
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


def wrap_angle(a: float) -> float:
    return math.atan2(math.sin(a), math.cos(a))


class SlamTourNode(Node):
    def __init__(self) -> None:
        super().__init__(
            "slam_mapping_tour",
            parameter_overrides=[Parameter("use_sim_time", value=True)],
        )
        self.pose: tuple[float, float, float] | None = None
        self.map_count = 0
        self.create_subscription(Odometry, "/odom", self.cb_odom, 10)
        self.create_subscription(OccupancyGrid, "/map", self.cb_map, 10)
        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)

    def cb_odom(self, msg: Odometry) -> None:
        p = msg.pose.pose.position
        yaw = quat_to_yaw(msg.pose.pose.orientation)
        self.pose = (p.x, p.y, yaw)

    def cb_map(self, _msg: OccupancyGrid) -> None:
        self.map_count += 1

    def publish_vel(self, vx: float, wz: float) -> None:
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_footprint"
        msg.twist.linear.x = float(vx)
        msg.twist.angular.z = float(wz)
        self.pub.publish(msg)

    def wait_ready(self, timeout_s: float = 20.0) -> None:
        t0 = time.monotonic()
        while time.monotonic() - t0 < timeout_s:
            rclpy.spin_once(self, timeout_sec=0.05)
            if self.pose is not None and self.map_count > 0:
                return
        raise RuntimeError(
            f"Timeout waiting for /odom and /map (pose={self.pose}, map_count={self.map_count})"
        )

    def go_to(self, gx: float, gy: float, tol: float = 0.18, timeout_s: float = 25.0) -> None:
        t0 = time.monotonic()
        next_pub = t0
        while time.monotonic() - t0 < timeout_s:
            rclpy.spin_once(self, timeout_sec=0.02)
            if self.pose is None:
                continue
            x, y, yaw = self.pose
            dx = gx - x
            dy = gy - y
            dist = math.hypot(dx, dy)
            if dist <= tol:
                self.publish_vel(0.0, 0.0)
                return

            target_yaw = math.atan2(dy, dx)
            err = wrap_angle(target_yaw - yaw)
            now = time.monotonic()
            if now >= next_pub:
                if abs(err) > 0.30:
                    wz = max(-1.0, min(1.0, 1.8 * err))
                    if abs(wz) < 0.25:
                        wz = math.copysign(0.25, wz)
                    self.publish_vel(0.0, wz)
                else:
                    vx = max(0.18, min(0.55, 0.85 * dist))
                    wz = max(-0.8, min(0.8, 1.4 * err))
                    self.publish_vel(vx, wz)
                next_pub = now + 0.05
        raise RuntimeError(f"Timeout driving to ({gx:.2f}, {gy:.2f}) from {self.pose}")

    def stop_and_settle(self, duration_s: float = 2.5) -> None:
        t0 = time.monotonic()
        while time.monotonic() - t0 < duration_s:
            self.publish_vel(0.0, 0.0)
            rclpy.spin_once(self, timeout_sec=0.05)


def measure_map_bounds(pgm_path: Path, yaml_path: Path) -> None:
    meta = {}
    for line in yaml_path.read_text(encoding="utf-8").splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    res = float(meta["resolution"])
    img = Image.open(pgm_path).convert("L")
    w, h = img.size
    px = img.load()

    xs: list[int] = []
    ys: list[int] = []
    for y in range(h):
        for x in range(w):
            if px[x, y] <= 10:
                xs.append(x)
                ys.append(y)
    if not xs or not ys:
        raise RuntimeError("No occupied wall cells found in saved SLAM map!")

    width_m = (max(xs) - min(xs) + 1) * res
    height_m = (max(ys) - min(ys) + 1) * res
    print(
        f"[MAP METRICS] Image: {w}x{h} px @ {res} m/px | "
        f"Measured room bounding box: {width_m:.2f}m x {height_m:.2f}m "
        f"(ground truth walls outer/center: 14.00m x 10.00m, "
        f"err_x={abs(width_m - 14.0):.2f}m, err_y={abs(height_m - 10.0):.2f}m)"
    )


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    maps_dir = repo_root / "ros2_ws" / "src" / "restaurant_robot_navigation" / "maps"
    maps_dir.mkdir(parents=True, exist_ok=True)
    map_prefix = maps_dir / "restaurant_floor_1"

    # Lộ trình khép kín đi qua toàn bộ khu vực nhà hàng tĩnh (xuất phát từ (0, 0))
    tour_waypoints = [
        (3.2, 0.0),
        (3.5, 3.5),
        (0.2, 3.6),
        (0.2, 0.0),
        (-2.6, 0.0),
        (-2.6, 2.2),
        (-4.4, 2.2),
        (-4.4, 3.8),
        (-4.4, 2.2),
        (-2.6, 2.2),
        (-2.6, -3.5),
        (-5.4, -3.5),
        (0.2, -3.6),
        (3.5, -3.6),
        (3.2, 0.0),
        (0.0, 0.0),
    ]

    rclpy.init()
    node = SlamTourNode()
    try:
        node.wait_ready()
        print(f"Start SLAM mapping tour from pose={node.pose}, map_msgs={node.map_count}")
        for idx, (wx, wy) in enumerate(tour_waypoints, start=1):
            node.go_to(wx, wy)
            print(f"  [{idx:02d}/{len(tour_waypoints):02d}] Reached ({wx:.2f}, {wy:.2f}), map_msgs={node.map_count}")
        node.stop_and_settle(2.5)
    finally:
        node.destroy_node()
        rclpy.shutdown()

    cmd = [
        "ros2",
        "run",
        "nav2_map_server",
        "map_saver_cli",
        "-f",
        str(map_prefix),
        "--ros-args",
        "-p",
        "use_sim_time:=true",
        "-p",
        "save_map_timeout:=10.0",
    ]
    print("Saving map:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    yaml_path = map_prefix.with_suffix(".yaml")
    pgm_path = map_prefix.with_suffix(".pgm")
    assert yaml_path.is_file() and pgm_path.is_file(), "Map files were not created!"
    measure_map_bounds(pgm_path, yaml_path)


if __name__ == "__main__":
    main()
