import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, SetParameter


def generate_launch_description():
    pkg_nav = get_package_share_directory("restaurant_robot_navigation")

    default_map = os.path.join(pkg_nav, "maps", "restaurant_floor_1.yaml")
    default_keepout = os.path.join(pkg_nav, "maps", "keepout_mask.yaml")
    default_speed = os.path.join(pkg_nav, "maps", "speed_mask.yaml")
    default_params = os.path.join(pkg_nav, "config", "nav2_params.yaml")
    filters_params = os.path.join(pkg_nav, "config", "costmap_filters.yaml")
    rviz_config = os.path.join(pkg_nav, "rviz", "nav2.rviz")

    use_sim_time = LaunchConfiguration("use_sim_time")
    autostart = LaunchConfiguration("autostart")
    map_yaml = LaunchConfiguration("map")
    keepout_mask_yaml = LaunchConfiguration("keepout_mask")
    speed_mask_yaml = LaunchConfiguration("speed_mask")
    params_file = LaunchConfiguration("params_file")
    use_rviz = LaunchConfiguration("use_rviz")

    localization_lifecycle_nodes = [
        "map_server",
        "amcl",
        "keepout_filter_mask_server",
        "keepout_costmap_filter_info_server",
        "speed_filter_mask_server",
        "speed_costmap_filter_info_server",
    ]

    navigation_lifecycle_nodes = [
        "controller_server",
        "smoother_server",
        "planner_server",
        "behavior_server",
        "bt_navigator",
        "waypoint_follower",
        "velocity_smoother",
        "collision_monitor",
    ]

    localization_group = GroupAction(
        actions=[
            SetParameter("use_sim_time", use_sim_time),
            Node(
                package="nav2_map_server",
                executable="map_server",
                name="map_server",
                output="screen",
                parameters=[params_file, {"yaml_filename": map_yaml}],
            ),
            Node(
                package="nav2_amcl",
                executable="amcl",
                name="amcl",
                output="screen",
                parameters=[params_file],
            ),
            Node(
                package="nav2_map_server",
                executable="map_server",
                name="keepout_filter_mask_server",
                output="screen",
                parameters=[filters_params, {"yaml_filename": keepout_mask_yaml}],
            ),
            Node(
                package="nav2_map_server",
                executable="costmap_filter_info_server",
                name="keepout_costmap_filter_info_server",
                output="screen",
                parameters=[filters_params],
            ),
            Node(
                package="nav2_map_server",
                executable="map_server",
                name="speed_filter_mask_server",
                output="screen",
                parameters=[filters_params, {"yaml_filename": speed_mask_yaml}],
            ),
            Node(
                package="nav2_map_server",
                executable="costmap_filter_info_server",
                name="speed_costmap_filter_info_server",
                output="screen",
                parameters=[filters_params],
            ),
            Node(
                package="nav2_lifecycle_manager",
                executable="lifecycle_manager",
                name="lifecycle_manager_localization",
                output="screen",
                parameters=[
                    {"use_sim_time": use_sim_time},
                    {"autostart": autostart},
                    {"node_names": localization_lifecycle_nodes},
                ],
            ),
        ]
    )

    navigation_group = GroupAction(
        actions=[
            SetParameter("use_sim_time", use_sim_time),
            Node(
                package="nav2_controller",
                executable="controller_server",
                output="screen",
                parameters=[params_file],
                remappings=[("cmd_vel", "cmd_vel_nav")],
            ),
            Node(
                package="nav2_smoother",
                executable="smoother_server",
                name="smoother_server",
                output="screen",
                parameters=[params_file],
            ),
            Node(
                package="nav2_planner",
                executable="planner_server",
                name="planner_server",
                output="screen",
                parameters=[params_file],
            ),
            Node(
                package="nav2_behaviors",
                executable="behavior_server",
                name="behavior_server",
                output="screen",
                parameters=[params_file],
                remappings=[("cmd_vel", "cmd_vel_nav")],
            ),
            Node(
                package="nav2_bt_navigator",
                executable="bt_navigator",
                name="bt_navigator",
                output="screen",
                parameters=[params_file],
            ),
            Node(
                package="nav2_waypoint_follower",
                executable="waypoint_follower",
                name="waypoint_follower",
                output="screen",
                parameters=[params_file],
            ),
            Node(
                package="nav2_velocity_smoother",
                executable="velocity_smoother",
                name="velocity_smoother",
                output="screen",
                parameters=[params_file],
                remappings=[("cmd_vel", "cmd_vel_nav")],
            ),
            Node(
                package="nav2_collision_monitor",
                executable="collision_monitor",
                name="collision_monitor",
                output="screen",
                parameters=[params_file],
            ),
            Node(
                package="nav2_lifecycle_manager",
                executable="lifecycle_manager",
                name="lifecycle_manager_navigation",
                output="screen",
                parameters=[
                    {"use_sim_time": use_sim_time},
                    {"autostart": autostart},
                    {"node_names": navigation_lifecycle_nodes},
                ],
            ),
        ]
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2_nav2",
        output="screen",
        arguments=["-d", rviz_config],
        parameters=[{"use_sim_time": use_sim_time}],
        condition=IfCondition(use_rviz),
    )

    return LaunchDescription(
        [
            SetEnvironmentVariable("RCUTILS_LOGGING_BUFFERED_STREAM", "1"),
            DeclareLaunchArgument("use_sim_time", default_value="true"),
            DeclareLaunchArgument("autostart", default_value="true"),
            DeclareLaunchArgument("map", default_value=default_map),
            DeclareLaunchArgument("keepout_mask", default_value=default_keepout),
            DeclareLaunchArgument("speed_mask", default_value=default_speed),
            DeclareLaunchArgument("params_file", default_value=default_params),
            DeclareLaunchArgument("use_rviz", default_value="false"),
            localization_group,
            navigation_group,
            rviz_node,
        ]
    )
