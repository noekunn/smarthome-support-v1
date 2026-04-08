---
title: Smarthome Support V1
emoji: 🏠
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 7860
---

# Smart-Home Support Desk Environment (SmartHomeSupportEnv)

A real-world environment where AI agents act as support desk representatives for a smart home device company.

## Motivation
Agents must prioritize tasks, manage device states, and communicate effectively with customers. This environment models the complexities of real-world support, including technical troubleshooting and security prioritization.

## Action Space (SmartHomeAction)
- `action_type`: `reply`, `search_docs`, `check_device_status`, `prioritize_ticket`, `close_ticket`
- `ticket_id`: Unique identifier for the ticket being handled.
- `content`: Text content for replies or search queries.
- `priority`: Numeric priority level (1-5).

## Observation Space (SmartHomeObservation)
- `open_tickets`: List of currently open tickets with details.
- `device_status`: Dictionary showing the status of relevant smart devices.
- `last_action_result`: Message confirming the result of the agent's previous action.
- `system_time`: Current simulation timestamp.

## Tasks
1.  **Password Reset (Easy)**: The agent must provide a specific password reset link to a customer.
2.  **Camera Offline (Medium)**: The agent must check the device status of a yard camera, confirm it is offline, and inform the customer about a restart.
3.  **Security Triage (Hard)**: The agent is presented with two tickets: one about a door lock being unlocked (High Priority) and one about a bulb color change (Low Priority). The agent must correctly prioritize and handle the security ticket first.

## Setup & Usage
1.  **Installation**: `pip install openenv-core pydantic openai`
2.  **Validation**: `openenv validate`
3.  **Baseline Inference**: `python inference.py`

## Baseline Scores
- Task 1: 1.00
- Task 2: 1.00
- Task 3: 1.00
- Average Score: 1.00
