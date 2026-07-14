# Reference Projects

Open-source projects/repos to guide each phase. Since we kept AR4 stock dimensions,
the AR4 stacks below are **largely reusable** (URDF, MoveIt, Gazebo, Isaac configs).

## By phase

| Phase | Reference | Notes |
|---|---|---|
| 1. CAD→URDF | [Ekumen-OS/ar4](https://github.com/Ekumen-OS/ar4), [ycheng517/ar4_ros_driver](https://github.com/ycheng517/ar4_ros_driver) | AR4 URDF — Ekumen covers Gazebo + Isaac + MuJoCo |
| 2. Gazebo | Ekumen/ar4 (Gazebo bringup), [MOGI-ROS Simple-arm](https://github.com/MOGI-ROS/Week-9-10-Simple-arm) | Jazzy + Gazebo Harmonic |
| 3. MoveIt/reach | [ar4 moveit config](https://github.com/ycheng517/ar4_ros_driver), [moveit2 MTC pick_place](https://github.com/moveit/moveit2_tutorials/tree/main/doc/tutorials/pick_and_place_with_moveit_task_constructor), [ros-industrial/reach_ros2](https://github.com/ros-industrial/reach_ros2) | MoveIt config + reachability |
| 4+5. Perception + task | [Franka Panda Color Sorting](https://github.com/MechaMind-Labs/Franka_Panda_Color_Sorting_Robot) (closest match), [UR3_ROS2_PICK_AND_PLACE](https://github.com/darshmenon/UR3_ROS2_PICK_AND_PLACE), [AR4 tabletop-handybot](https://github.com/ycheng517/tabletop-handybot) | HSV color-sort + RGB-D→IK; AR4 pick-place |
| 6. Isaac + policy | Ekumen/ar4 (Isaac port), [huggingface/lerobot](https://github.com/huggingface/lerobot), [lerobot-mujoco-tutorial](https://github.com/jeongeun980906/lerobot-mujoco-tutorial), [Isaac Lab](https://github.com/isaac-sim/IsaacLab) (Mimic) | VLA/imitation policy |

**Closest single project to our task:** the Franka Panda Color Sorting Robot — HSV
detection → MoveIt 2 IK → place in colored bins, in Gazebo, ROS 2. Does 3 colors;
extending to 6 is a config change.

## CAD learning references

- Playlist (from scratch, beginner): https://www.youtube.com/playlist?list=PL_gRt21XQOIkdyAbR8tRXAgVEyxzADyul
- 6-axis series (2025): https://www.youtube.com/watch?v=IchHC7Ue8X8
- Native SolidWorks parts (editable) on GrabCAD: https://grabcad.com/library/6-dof-robotic-arm-tutorials-1
- sw2urdf written guide (pitfalls): https://robocademy.com/blog/converting-solidworks-cad-models-to-urdf
- AR4 CAD (STL, dimensional reference): https://anninrobotics.com/downloads

## Job-market context

Skill-demand surveys that informed tech choices live outside the repo at
`~/job_search/*.html` (robotics / AI-ML / embedded role skill frequencies).
