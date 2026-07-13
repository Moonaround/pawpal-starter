import pytest
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

def test_task_completion_and_recurrence_logic():
    """Verify that marking a daily task complete returns a new task twin exactly 1 day later."""
    base_time = datetime(2026, 5, 20, 8, 0)
    task = Task("rec_01", "Mochi", "Feeding", "Breakfast", base_time, 15, "High", "Daily")
    
    assert task.is_completed is False
    
    # Process the task completion event
    next_task = task.mark_complete()
    
    assert task.is_completed is True
    assert next_task is not None
    assert next_task.title == "Feeding"
    # Prove interval addition arithmetic: 8:00 AM today vs 8:00 AM tomorrow
    assert next_task.date_time == base_time + timedelta(days=1)

def test_sorting_correctness_chronological():
    """Verify that get_daily_tasks always extracts records ordered chronologically by execution time."""
    owner = Owner("Jordan", "jordan@example.com")
    mochi = Pet("Mochi", "Dog", 2)
    owner.add_pet(mochi)
    
    today = datetime(2026, 5, 20)
    # Instantiate tasks out of order intentionally
    t_evening = Task("t1", "Mochi", "Brush", "Groom", today + timedelta(hours=18), 15, "Low")
    t_morning = Task("t2", "Mochi", "Walk", "Run", today + timedelta(hours=8), 30, "High")
    
    mochi.add_task(t_evening)
    mochi.add_task(t_morning)
    
    scheduler = Scheduler()
    scheduler.sync_tasks_from_owner(owner)
    daily_list = scheduler.get_daily_tasks(today)
    
    # Assertions prove chronological sorting reordering rules worked
    assert len(daily_list) == 2
    assert daily_list[0].task_id == "t2"  # 8:00 AM must precede 6:00 PM
    assert daily_list[1].task_id == "t1"

def test_conflict_detection_logic():
    """Verify that overlapping intervals trigger a positive warning flag within the scheduling container."""
    owner = Owner("Jordan", "jordan@example.com")
    mochi = Pet("Mochi", "Dog", 2)
    owner.add_pet(mochi)
    
    today = datetime(2026, 5, 20, 9, 0)
    # task 1 runs from 9:00 AM to 9:30 AM
    task1 = Task("tk1", "Mochi", "Morning Vet", "Checkup", today, 30, "High")
    # task 2 runs from 9:15 AM to 9:25 AM (inside task 1 timeframe)
    task2 = Task("tk2", "Mochi", "Give Pill", "Meds", today + timedelta(minutes=15), 10, "High")
    
    mochi.add_task(task1)
    mochi.add_task(task2)
    
    scheduler = Scheduler()
    scheduler.sync_tasks_from_owner(owner)
    conflicts = scheduler.detect_conflicts()
    
    assert len(conflicts) == 1
    assert conflicts[0][0].task_id == "tk1"
    assert conflicts[0][1].task_id == "tk2"

def test_capacity_filtering_edge_case():
    """Verify scheduler drops tasks cleanly if duration totals exceed max time capacity allocation limits."""
    scheduler = Scheduler()
    today = datetime(2026, 5, 20, 10, 0)
    
    task1 = Task("tk1", "Mochi", "Park Run", "Exercise", today, 60, "High")
    task2 = Task("tk2", "Mochi", "Grooming", "Wash", today + timedelta(hours=2), 60, "Medium")
    
    scheduler.tasks.extend([task1, task2])
    # Allocate only 90 minutes of total capacity, which is short of the 120 required
    scheduled, skipped = scheduler.generate_plan(today, 90)
    
    assert len(scheduled) == 1
    assert scheduled[0].task_id == "tk1"
    assert len(skipped) == 1
    assert skipped[0].task_id == "tk2"
