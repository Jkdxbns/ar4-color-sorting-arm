"""
This is the launch file for the AR4 arm Gazebo simulation.

The following are libraries used to create the AR4 arm Gazebo launch file.
"""
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command

from launch_ros.actions import Node

"""
The following function generates the launch description for the AR4 arm.
"""


def generate_launch_description():
    """Create and return the launch description for the AR4 arm."""
    # Define the paths to packages and files.
    gazebo_pkg = get_package_share_directory('ar4_robot_arm_gazebo')
    description_pkg = get_package_share_directory('ar4_robot_arm_description')
    ros_gz_sim_pkg = get_package_share_directory('ros_gz_sim')

    world_file = os.path.join(gazebo_pkg, 'worlds', 'empty.world')
    urdf_file = os.path.join(description_pkg, 'urdf', 'ar4_robot_arm.urdf')

    # Set up Gazebo resource path to find the robot arm's meshes.
    gz_resource_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.join(description_pkg, '..')
    )

    # Include the Gazebo launch file.
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_pkg, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': f'-r -v 4 {world_file}'
        }.items()
    )

    # Bridge for simulation clock synchronization.
    gazebo_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        output='screen'
    )

    # Start the robot state publisher node.
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_file])
        }]
    )

    # Spawn the robot arm in Gazebo.
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'ar4_robot_arm',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.0',
            '-Y', '3.14159'
        ],
        output='screen'
    )

    # Start the joint state broadcaster.
    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '-c',
            '/controller_manager'
        ]
    )

    # Start the joint trajectory controller.
    joint_trajectory_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_trajectory_controller',
            '-c',
            '/controller_manager'
        ]
    )

    # Create the launch description and populate.
    ld = LaunchDescription()

    # Declare the launch options.
    ld.add_action(gz_resource_path)
    ld.add_action(gazebo)
    ld.add_action(gazebo_bridge)
    ld.add_action(robot_state_publisher)
    ld.add_action(spawn_robot)
    ld.add_action(joint_state_broadcaster)
    ld.add_action(joint_trajectory_controller)

    return ld
