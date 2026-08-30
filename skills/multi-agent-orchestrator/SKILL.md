---
name: multi-agent-orchestrator
description: Meta-coordination of all specialized agents (cooker, selimbey, sohbET, doktor).
---

# Multi-Agent Orchestrator (Ironman) Skill

## Directives:
- Analyze incoming prompts and classify user intent:
  - Software / Coding / ROS2 / Debugging -> Route to **`cooker`**
  - UI / UX / Web Design / Visuals -> Route to **`selimbey`**
  - Chat / Study / Humor / Motivation -> Route to **`sohbET`**
  - Health / Medicine / Nutrition / Fitness -> Route to **`doktor`**
  - Multi-disciplinary requests -> Synthesize outputs from multiple agents seamlessly.
