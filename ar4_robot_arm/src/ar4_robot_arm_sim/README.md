# ar4_robot_arm_sim

Runs the AR4 arm in Gazebo with `ros2_control`. The arm holds its pose against
gravity and follows joint commands.

Meshes come from `ar4_robot_arm_description`. This package owns the control
wiring, the controller config and the launch files.

## What each file does

| File | Role |
|---|---|
| `urdf/ar4_robot_arm.control.urdf` | The arm plus a `<ros2_control>` block using the `gz_ros2_control/GazeboSimSystem` plugin. All 6 joints expose a `position` command interface and `position` + `velocity` state interfaces. Adds a `world` link and a fixed joint into it so the base stays anchored. |
| `config/controllers.yaml` | `controller_manager` at 100 Hz, running `joint_state_broadcaster` and `joint_trajectory_controller` over the 6 joints. |
| `launch/bringup_gazebo.launch.py` | The launch file to use. Starts `robot_state_publisher`, Gazebo with physics running, the `/clock` bridge, spawns the arm and starts both controllers. |
| `launch/view_gazebo.launch.py` | Loads the model with no physics and no controllers. The arm droops. Use it only to check the model loads. |
| `urdf/ar4_robot_arm.gazebo.urdf` | The model without control wiring, used by `view_gazebo.launch.py`. |

Gazebo runs on the `bullet-featherstone` physics engine here. The default engine
does not handle the mesh arm well.

## Requirements

ROS 2 Jazzy, plus:

```bash
sudo apt install ros-jazzy-ros2-control ros-jazzy-ros2-controllers \
                 ros-jazzy-gz-ros2-control ros-jazzy-ros-gz
```

## Run it

```bash
# 1. get the code
git clone git@github.com:Jkdxbns/ar4-color-sorting-arm.git
cd ar4-color-sorting-arm
git checkout ros2

# 2. pull the meshes (they are stored in Git LFS, a plain clone gives you
#    131 byte placeholder files and the arm renders as nothing)
git lfs install
git lfs pull

# 3. build
cd ar4_robot_arm
colcon build
source install/setup.bash

# 4. launch
ros2 launch ar4_robot_arm_sim bringup_gazebo.launch.py
```

Gazebo opens with the arm standing upright and holding position.

## Confirm the controllers came up

In a second terminal, from the same `ar4_robot_arm` directory:

```bash
source install/setup.bash
ros2 control list_controllers
```

Both should report `active`:

```
joint_state_broadcaster      joint_state_broadcaster/JointStateBroadcaster      active
joint_trajectory_controller  joint_trajectory_controller/JointTrajectoryController  active
```

## Move the arm

```bash
ros2 topic pub --once /joint_trajectory_controller/joint_trajectory \
  trajectory_msgs/msg/JointTrajectory \
  "{joint_names: [joint_1, joint_2, joint_3, joint_4, joint_5, joint_6],
    points: [{positions: [0.5, 0.3, 0.3, 0.5, -0.5, 0.5],
              time_from_start: {sec: 3}}]}"
```

The arm moves to that pose over 3 seconds and holds it. Send all zeros to
return it to the start pose.

Joint limits, in radians:

| Joint | Lower | Upper |
|---|---|---|
| joint_1 | 0.0 | 6.283185 |
| joint_2 | -0.785398 | 1.570796 |
| joint_3 | -0.785398 | 1.570796 |
| joint_4 | 0.0 | 6.283185 |
| joint_5 | -3.403392 | 0.261799 |
| joint_6 | 0.0 | 6.283185 |

Commands outside these are clamped by the controller.

## If something does not work

| Symptom | Cause |
|---|---|
| Arm is invisible or Gazebo reports mesh errors | `git lfs pull` was not run, so the meshes are LFS pointer files |
| `ros2 control list_controllers` returns nothing | `controller_manager` is not up, check the launch output for the spawner nodes |
| Arm spawns then collapses | The controllers did not load, so nothing is holding the joints |
| `Package 'ar4_robot_arm_sim' not found` | `source install/setup.bash` was not run in that terminal |
