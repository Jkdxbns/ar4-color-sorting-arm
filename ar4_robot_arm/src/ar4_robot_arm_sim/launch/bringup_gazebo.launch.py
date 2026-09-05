"""Step 1 bringup: the arm in Gazebo with working controllers.

Difference from view_gazebo.launch.py: this one RUNS physics (-r) and loads
controllers, so the arm HOLDS its pose instead of drooping, and you can command it.

Nodes:
  robot_state_publisher    - publishes the control URDF + TF
  gz_sim (included)        - Gazebo Harmonic, RUNNING, bullet-featherstone physics
  clock bridge             - feeds Gazebo's clock to ROS (controllers need sim time)
  create                   - spawns the arm into Gazebo
  jsb spawner              - starts joint_state_broadcaster
  jtc spawner              - starts joint_trajectory_controller
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

URDF = os.path.join(
    get_package_share_directory("ar4_robot_arm_sim"), "urdf", "ar4_robot_arm.control.urdf"
)


def generate_launch_description():
    controllers_yaml = os.path.join(
        get_package_share_directory("ar4_robot_arm_sim"), "config", "controllers.yaml"
    )
    with open(URDF, "r") as f:
        # the gz_ros2_control plugin needs a real filesystem path, not package://
        robot_description = f.read().replace("__CONTROLLERS_YAML__", controllers_yaml)

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch", "gz_sim.launch.py"
            )
        ),
        # -r = RUN physics (not paused); bullet-featherstone handles the mesh arm well
        launch_arguments={
            "gz_args": "-r -v 3 --physics-engine gz-physics-bullet-featherstone-plugin empty.sdf"
        }.items(),
    )

    # Gazebo's /clock -> ROS, so controllers using use_sim_time stay in sync
    clock_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"],
        output="screen",
    )

    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-name", "ar4_robot_arm", "-topic", "robot_description", "-z", "0.0"],
    )

    jsb_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "-c", "/controller_manager",
                   "--controller-manager-timeout", "60"],
        output="screen",
    )

    jtc_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller", "-c", "/controller_manager",
                   "--controller-manager-timeout", "60"],
        output="screen",
    )

    return LaunchDescription([
        robot_state_publisher,
        gz_sim,
        clock_bridge,
        spawn,
        jsb_spawner,
        jtc_spawner,
    ])
