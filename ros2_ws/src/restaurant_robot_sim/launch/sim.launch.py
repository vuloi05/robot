import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
    RegisterEventHandler,
    SetEnvironmentVariable,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    pkg_desc = get_package_share_directory("restaurant_robot_description")
    pkg_sim = get_package_share_directory("restaurant_robot_sim")
    pkg_nav = get_package_share_directory("restaurant_robot_navigation")
    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")

    headless = LaunchConfiguration("headless").perform(context).lower() == "true"
    static_world = LaunchConfiguration("static_world").perform(context).lower() == "true"
    use_rviz = LaunchConfiguration("use_rviz").perform(context).lower() == "true"
    use_ekf = LaunchConfiguration("use_ekf").perform(context).lower() == "true"
    x_pose = LaunchConfiguration("x_pose").perform(context)
    y_pose = LaunchConfiguration("y_pose").perform(context)
    yaw_pose = LaunchConfiguration("yaw_pose").perform(context)

    world_name = "restaurant_static.sdf" if static_world else "restaurant.sdf"
    world_file = os.path.join(pkg_sim, "worlds", world_name)
    models_dir = os.path.join(pkg_sim, "models")
    bridge_cfg = os.path.join(pkg_sim, "config", "gz_bridge.yaml")
    ekf_cfg = os.path.join(pkg_nav, "config", "ekf.yaml")
    rviz_cfg = os.path.join(pkg_desc, "rviz", "view_robot.rviz")
    xacro_file = os.path.join(pkg_desc, "urdf", "restaurant_robot.urdf.xacro")

    robot_description_xml = xacro.process_file(xacro_file).toxml()

    existing_gz_res = os.environ.get("GZ_SIM_RESOURCE_PATH", "")
    gz_res_path = os.pathsep.join([p for p in [models_dir, existing_gz_res] if p])

    gz_args = f"-r -s {world_file}" if headless else f"-r {world_file}"

    actions = [
        SetEnvironmentVariable(name="GZ_SIM_RESOURCE_PATH", value=gz_res_path),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")
            ),
            launch_arguments={
                "gz_args": gz_args,
                "on_exit_shutdown": "true",
            }.items(),
        ),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[
                {
                    "robot_description": robot_description_xml,
                    "use_sim_time": True,
                }
            ],
        ),
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            name="ros_gz_bridge",
            output="screen",
            parameters=[
                {
                    "config_file": bridge_cfg,
                    "use_sim_time": True,
                }
            ],
        ),
    ]

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-name",
            "restaurant_robot",
            "-topic",
            "robot_description",
            "-x",
            x_pose,
            "-y",
            y_pose,
            "-z",
            "0.01",
            "-Y",
            yaw_pose,
        ],
    )
    actions.append(spawn_robot)

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        output="screen",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "30",
        ],
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        output="screen",
        arguments=[
            "diff_drive_controller",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "30",
            "--controller-ros-args",
            "-r /diff_drive_controller/cmd_vel:=/cmd_vel",
            "--controller-ros-args",
            "-r /diff_drive_controller/odom:=/wheel_odom",
        ],
    )

    actions.append(
        RegisterEventHandler(
            OnProcessExit(
                target_action=spawn_robot,
                on_exit=[joint_state_broadcaster_spawner],
            )
        )
    )
    actions.append(
        RegisterEventHandler(
            OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[diff_drive_spawner],
            )
        )
    )

    if use_ekf:
        actions.append(
            Node(
                package="robot_localization",
                executable="ekf_node",
                name="ekf_filter_node",
                output="screen",
                parameters=[ekf_cfg, {"use_sim_time": True}],
                remappings=[("odometry/filtered", "/odom")],
            )
        )

    if use_rviz:
        actions.append(
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=["-d", rviz_cfg],
                parameters=[{"use_sim_time": True}],
            )
        )

    return actions


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "headless",
                default_value="false",
                description="Run Gazebo Harmonic server without GUI (-s) when true",
            ),
            DeclareLaunchArgument(
                "static_world",
                default_value="false",
                description="Use static world without moving pedestrians for clean SLAM mapping",
            ),
            DeclareLaunchArgument(
                "use_rviz",
                default_value="false",
                description="Launch RViz2 alongside simulation",
            ),
            DeclareLaunchArgument(
                "use_ekf",
                default_value="true",
                description="Run robot_localization EKF node fusing /wheel_odom and /imu/data",
            ),
            DeclareLaunchArgument("x_pose", default_value="-5.50"),
            DeclareLaunchArgument("y_pose", default_value="-3.60"),
            DeclareLaunchArgument("yaw_pose", default_value="0.0"),
            OpaqueFunction(function=launch_setup),
        ]
    )
