import pytest
from datetime import datetime
from pawpal_system import Pet, Task

def test_task_completion():
    """Verify that calling mark_complete() changes the completion status flag."""
    task = Task("t1", "Biscuit", "Feeding", "Breakfast", datetime.now(), 15, "High")
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's inner task tracking list count."""
    pet = Pet("Biscuit", "Dog", 3)
    task = Task("t1", "Biscuit", "Walk", "Park run", datetime.now(), 30, "Medium")
    
    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1
