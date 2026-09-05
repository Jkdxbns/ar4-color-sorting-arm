"""Minimal launch: show Sahil's arm standing in Gazebo Harmonic (paused).

Three nodes:
  - robot_state_publisher : reads the URDF, publishes /robot_description + TF frames.
  - gz_sim (included)     : starts Gazebo Harmonic with an empty world, PAUSED (no -r flag).
  - create               : spawns the arm from the /robot_description topic into Gazebo.

No controllers here -> once you press play, gravity will make the joints droop.
That's expected; adding ros2_control is the next step.
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

URDF = os.path.join(
    get_package_share_directory("ar4_robot_arm_sim"), "urdf", "ar4_robot_arm.gazebo.urdf"
)


def generate_launch_description():
    with open(URDF, "r") as f:
        robot_description = f.read()

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch", "gz_sim.launch.py"
            )
        ),
        # -v 4 = verbose logs; empty.sdf = builtin empty world; NO -r = start paused.
        launch_arguments={"gz_args": "-v 4 empty.sdf"}.items(),
    )

    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-name", "ar4_robot_arm", "-topic", "robot_description", "-z", "0.0"],
    )

    return LaunchDescription([robot_state_publisher, gz_sim, spawn])
