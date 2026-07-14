# Meeting Notes

## June 27
Project start proposal sent on Discord; working in groups suggested.

## June 29
Discussed kinds of robots and major manipulator applications (car assembly, package
assembly, warehouse maintenance, medical) and their main features (object detection &
segregation, hard-coded pick-and-place, lidar-based).

## July 06 — Phase-1 M1
- Tooling: Docs + GitHub throughout the project.
- Selected task: **object pick and place**.
- Features discussed:
  a. Object detection and tracking
  b. Mobile arm (pick and place) for segregation
  c. Mobile arm for room sorting/cleaning
  d. Legged (spider) robot using front legs as end effectors, working in swarm
  e. Assembly robot with mm-level precision
  f. Stationary object detection pick and place

## July 10 — Phase-1 M2
- Decided to use an existing arm as CAD guide; prefer a project that designed +
  simulated + trained (incl. Isaac Sim) so we can redo and adapt it.
- Feature ideas: pick/drop cube in a zone; sort cubes into matching bins; stack cubes.
- Actuators, 2-finger end effector, touch sensor, RGB-D camera with HSV+depth pose.
- Inspiration: **AR4**. CAD tools: SolidWorks + AutoCAD + Fusion.
- **FINALIZED TASK:** detect object + pick + place in bins — same-sized boxes, different
  colors; segregate from one base bin into colored bins.
- Dimensions locked (see `design-spec.md`): 2-finger claw; 6 colors; 42 boxes;
  5 cm boxes; bins 25×25×50 cm; base bin 1 m³; boxes < 0.5 kg.

## Later decisions (post-July-10)
- ROS 2 Jazzy, Docker, Git/PR workflow.
- **Arm kept at AR4 stock dimensions (~600 mm reach)** so AR4 reference stacks stay
  reusable. Bins moved in to ~0.5 m (from 1 m) so the arm reaches them.
- Dropped 1D lidar in favor of wrist RGB-D camera.
- Grasp sensing: limit switch (CAD) → contact sensor + joint-effort (sim).
- CAD designed from scratch, parametric, per-person subassemblies.
