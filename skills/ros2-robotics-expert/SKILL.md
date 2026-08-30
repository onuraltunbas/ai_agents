---
name: ros2-robotics-expert
description: Deep expertise in ROS2 Humble/Jazzy, lifecycle nodes, TF2, Nav2, CAN driver protocols, and kinematics.
---

# ROS2 & Robotics Skill

## Directives:
- Use standard ROS2 package structures (`package.xml`, `CMakeLists.txt` or `setup.py`).
- Prefer composition and lifecycle nodes over monolithic nodes.
- When working with angles and quaternions, always handle boundary wrapping ($[-\pi, \pi]$) to prevent gimbal lock/yaw jumps.
- Write robust real-time CAN/Serial framing parsers with state machines and CRC checks.
