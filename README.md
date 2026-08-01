# 6DOF Robot Arm - Color Box Segregation

A 6-DOF robotic arm that detects colored boxes and sorts them into matching bins. The
arm is designed in CAD, simulated in Gazebo, motion-planned with MoveIt 2, and driven by
a camera (RGB-D with color detection), then moved into Isaac Sim for a learned policy.
Simulation only.

## Task

Sort 42 boxes (5x5x5 cm, six colors: Red, Blue, Green, Black, White, Light Blue) from
one base bin into six colored bins. AR4-based arm, two-finger gripper, wrist-mounted
RGB-D camera.

## Stack

- CAD: SolidWorks + Fusion 360, exported to URDF with sw2urdf
- Middleware: ROS 2 Jazzy
- Simulation: Gazebo, then Isaac Sim
- Motion planning: MoveIt 2
- Perception: RGB-D with HSV/YOLO color detection and IK

## Contents

- CAD - arm design files (native and shared STEP)

## CAD exchange format

STEP (.step / .stp) is the shared format between SolidWorks and Fusion 360. Native files
(.SLDPRT, .SLDASM, .f3d) are kept alongside.

## Repository workflow

CAD files use Git LFS, so run `git lfs install` after cloning. Branch from main as
feature/<name>, open a pull request, and merge after review.
