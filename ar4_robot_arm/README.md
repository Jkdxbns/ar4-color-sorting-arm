# AR4 Robot Arm
This is the ROS 2 project folder of the AR4 Robot Arm.

To install each packages' dependencies, execute the following commands in your ROS 2 workspace directory:
```
rosdep update
rosdep install --from-paths src -y --ignore-src
```

This project was tested using ROS 2 Jazzy and Ubuntu 24.04. Store the project folder in the `src` directory of your ROS 2 workspace directory, and include the following in your `~/.bashrc` file:
```
source /opt/ros/jazzy/setup.bash
export LIBGL_ALWAYS_SOFTWARE=1
export QT_QPA_PLATFORM=xcb
source ~/{your ROS 2 workspace name}/install/setup.bash
export GZ_IP=127.0.0.1
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:/home/{username}/{your ROS 2 workspace name}/install/ar4_robot_arm/share
```

Then build the packages while you are in your ROS 2 workspace directory:
```
colcon build --packages-select ar4_robot_arm_description ar4_robot_arm_driver ar4_robot_arm_gazebo
```

To open the AR4 arm in RViz, execute this command:
```
ros2 launch ar4_robot_arm_description rviz.launch.py
```