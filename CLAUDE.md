# CLAUDE.md — 6DOF Robot Arm Project

Guidance for Claude Code sessions in this repo. **Living document** — update it as
decisions are made and phases progress. Only records what the team has actually
decided; don't add speculative detail.

## What this project is

A 6-DOF robotic arm (simulation-only) that detects colored boxes and sorts them into
matching bins. Full pipeline: CAD → URDF → Gazebo → MoveIt 2 → vision/IK → (later)
Isaac Sim + learned policy. 6-person team, everyone rotates roles each phase.

## Current status

**Phase 1 — CAD.** Designing the arm from scratch in SolidWorks/Fusion 360.
Only CAD is in scope right now; later phases get added to the repo as they start.

## Locked decisions

- **Simulation-only** (no physical hardware).
- **ROS 2 Jazzy** as middleware.
- **Arm: AR4-based 6DOF, stock AR4 dimensions (~600 mm reach).** We keep AR4's
  dimensions so its reference URDF/ROS stacks (Ekumen, ycheng) stay largely reusable.
  CAD is still designed **from scratch, parametrically**, so parts can be changed later.
- **Bins moved in to ~0.5 m** (was 1 m) so the ~600 mm arm can reach them. ⚠️ This
  revises the July-10 dimension — confirm exact distances with the team.
- **Sensing: wrist-mounted RGB-D camera.** 1D lidar dropped.
- **End effector: 2-finger parallel claw**, >60 mm jaw travel, fingertip limit switch.
- **Grasp detection (in sim): contact sensor + joint-effort**, plus a Gazebo grasp-fix
  plugin (Gazebo grippers drop objects otherwise).
- **CAD interchange format: STEP (`.step`/`.stp`)** — SolidWorks + Fusion both read it.

See [`docs/design-spec.md`](docs/design-spec.md) for full task + design detail.

## Stack

CAD (SolidWorks + Fusion 360) → `sw2urdf` → URDF · ROS 2 Jazzy · Gazebo → Isaac Sim ·
MoveIt 2 · RGB-D + HSV/YOLO color detection + IK.

## Repo structure

```
CLAUDE.md         This file — project context + rules
README.md         Public-facing summary
CAD/              Arm design files (native + shared STEP)
docs/
  design-spec.md         Locked task + design specification
  meeting-notes.md       Team meeting log
  research-references.md  Reference projects/repos by phase
```
(Folders for `urdf/`, `ros2_ws/` get added when those phases start.)

## CAD conventions (Phase 1)

- **Design from scratch, parametric.** Drive dimensions from SolidWorks global
  variables / design tables (`link_length`, `motor_width`, `bearing_bore`, etc.) so
  parts can be re-scaled without redrawing.
- **Frames for URDF export:** put all reference coordinate systems + axes at the
  **assembly (.SLDASM) level**, with each joint's **Z-axis = its motion axis**.
- **Assign a material to every part** or mass/inertia exports as zero.
- **Suppress fasteners/cosmetics** before export (they wreck inertia).
- Export each subassembly as **STEP**; PM integrates into one master assembly.
- CAD binaries are stored via **Git LFS** (`git lfs install` after cloning).

## Git workflow

- Remote is SSH (`git@github.com:Jkdxbns/GithubTeamProject.git`).
- Work on `feature/<name>` branches → open a PR → one review → merge to `main`.
- Team members need a **collaborator invite** (Settings → Collaborators) to push —
  merging a PR does not grant access.

## Updating this file

When a decision is made or a phase starts, add it to the relevant section here and to
`docs/`. Keep entries factual and dated where useful.
