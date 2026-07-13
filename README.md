# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

To validate the algorithmic logic layers, schedule sorting correctness, boundary limit constraints, overlapping intervals, and recurring task generation routines, execute the suite via terminal command line:

```bash
python -m pytest -v
```

### Successful Test Run Execution Output Logs:
```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/jap/Documents/Codepath/AI110/pawpal-starter/pawpal-starter
collected 4 items

tests/test_pawpal.py::test_task_completion_and_recurrence_logic PASSED   [ 25%]
tests/test_pawpal.py::test_sorting_correctness_chronological PASSED     [ 50%]
tests/test_pawpal.py::test_conflict_detection_logic PASSED               [ 75%]
tests/test_pawpal.py::test_capacity_filtering_edge_case PASSED           [100%]

============================== 4 passed in 0.04s ===============================
```

### System Reliability Rating:
⭐⭐⭐⭐⭐ (5/5 Stars) — Core routines undergo programmatic testing across edge criteria, handling structural boundaries gracefully.


## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.get_daily_tasks()` | Sorts items primarily by start time via lambda, cascading to priority ranking. |
| Filtering | `Pet.get_filtered_tasks()` | Allows isolation of care records based on custom completion boolean flags. |
| Conflict handling | `Scheduler.detect_conflicts()` | Implements bounding interval comparison equations to pinpoint concurrent booking. |
| Recurring tasks | `Task.mark_complete()` | Employs timedelta vector projections to recreate new task twins for future dates. |

## 📸 Demo Walkthrough

Follow these instructions to experience the full automated capabilities of the PawPal+ application interface:

1. **Configure Profiles:** Input the manager's name and choose a default care recipient (e.g., set the Pet Name field to `Mochi` and select species `dog`). 
2. **Inject Scheduling Telemetry:** Enter a Task Title (e.g., `Morning walk`), adjust the duration tracker slider to `30` minutes, set the priority selection box to `high`, and click the **Add task** button. The application updates memory instantly and displays your new entry inside the backend tracking data matrix.
3. **Trigger Time Capacity Constraints:** Use the time slider to restrict your total calendar availability for the day. Click the **Generate schedule** button. The optimization scheduler reads incoming items, evaluates capacity limits, chronologically sorts elements, and highlights exactly what tasks fit or what entries were safely skipped due to capacity caps.
4. **Inspect Validation Overlaps:** Add an extra care task at an identical or overlapping timeline slot. The layout interface instantly flashes a bright red validation banner indicating a **Schedule Time Conflict** error, keeping your daily care routine organized and collision-free.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
