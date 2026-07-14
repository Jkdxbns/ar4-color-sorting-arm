# Design Specification

Locked design and task spec. Update as decisions change.

## Task

Detect colored boxes, pick them from a base bin, and segregate them into matching
colored bins. Simulation-only.

| Item | Spec |
|---|---|
| Boxes | 42 total, 7 each of 6 colors |
| Colors | Red, Blue, Green, Black, White, Light Blue |
| Box size | 5 × 5 × 5 cm, < 0.5 kg each |
| Colored bins | 6 × (25 × 25 × 50 cm, L×W×H), one per color |
| Base bin | 1 × 1 × 1 m |
| Bin distance | **~0.5 m** from base center (revised from 1 m — see note); base bin slightly closer |

> **Reach note:** original spec put bins at 1 m, but we kept AR4's stock ~600 mm reach,
> so bins were moved in to ~0.5 m. Confirm exact distances with the team.

> **Color note:** Black/White/Light-Blue are low-saturation and hard for HSV hue
> thresholding — perception will likely need value-channel logic for these.

## Arm

- **6 DOF**, revolute (yaw–pitch–pitch–roll–pitch–roll).
- **AR4-based, stock AR4 dimensions (~600 mm reach).** Kept as-is so AR4 reference
  URDF/ROS stacks (Ekumen, ycheng) remain largely reusable.
- **CAD designed from scratch, parametric** — AR4 is the dimensional reference; we
  re-model parts so the team learns CAD and can change dimensions later.
- **Actuator sizing (AR4-class):** larger steppers at J1–J3 (base/shoulder/elbow, which
  carry the most load), smaller at J4–J6 (wrist).

## End effector & sensing

- **2-finger parallel claw**, > 60 mm jaw travel (clears a 50 mm box). Second finger is
  a URDF `mimic` joint, not a physical closed loop.
- **Fingertip limit-switch** link (in sim → contact sensor).
- **Wrist-mounted RGB-D camera** (eye-in-hand). 1D lidar dropped.
- **Grasp detection in sim:** contact sensor + joint-effort spike; add a Gazebo
  grasp-fix plugin so grasped boxes don't slip out of the gripper.

## CAD work split (6 people, one subassembly each)

| Owner | Subassembly | Contains |
|---|---|---|
| A | Base + turntable | Fixed base, J1 yaw housing + motor |
| B | Shoulder | Link 1, J2 pitch, motor/bracket |
| C | Upper arm | Link 2, J3 pitch, motor/bracket |
| D | Forearm | Link 3, J4 roll, motor/bracket |
| E | Wrist | Links 4+5, J5 & J6, flange |
| F | End effector + sensors | 2-finger claw, fingertip switch, RGB-D mount + body |

**PM owns** the master assembly, the interface sheet (junction faces + frame
convention), and the `sw2urdf` export.

## CAD export formats

| Format | Purpose |
|---|---|
| `.SLDPRT` / `.SLDASM` / `.f3d` | Native editable source (per tool) |
| **`.STEP` / `.stp`** | Shared interchange (SolidWorks ↔ Fusion) + master assembly |
| URDF + `.STL`/`.dae` | Simulation (Gazebo/MoveIt/Isaac), from `sw2urdf` |

## sw2urdf export pitfalls (checklist)

- Every part has a material/density assigned (else zero inertia).
- All mates, coordinate systems, and axes at `.SLDASM` level, not inside parts.
- Each joint: Z-axis aligned to motion axis.
- Keep the `meshes/` folder beside the URDF (relative paths).
- Expect a ~90° global RPY correction in RViz.
- `sw2urdf` ships no controllers — add ros2_control YAML separately.
