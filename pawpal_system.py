from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import datetime, timedelta

@dataclass
class Task:
    task_id: str
    pet_name: str
    title: str
    description: str
    date_time: datetime
    duration_minutes: int
    priority: str  # "High", "Medium", "Low"
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed by switching its status flag."""
        self.is_completed = True

    @property
    def end_time(self) -> datetime:
        """Calculate the exact end time based on start time and duration."""
        return self.date_time + timedelta(minutes=self.duration_minutes)

    @property
    def priority_value(self) -> int:
        """Convert string priority to a numeric value for chronological sorting."""
        mapping = {"High": 3, "Medium": 2, "Low": 1}
        return mapping.get(self.priority, 0)

@dataclass
class Pet:
    name: str
    species: str
    age: int
    medical_notes: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a specific care task directly to this pet's itinerary."""
        self.tasks.append(task)

class Owner:
    def __init__(self, name: str, email: str):
        self.name: str = name
        self.email: str = email
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a new registered pet to the owner's profile profile."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet profile from management by its name string."""
        self.pets = [p for p in self.pets if p.name != pet_name]

class Scheduler:
    def __init__(self):
        """Initialize the scheduling manager engine."""
        self.tasks: List[Task] = []

    def sync_tasks_from_owner(self, owner: Owner) -> None:
        """Gather and centralize all tasks across all pets registered under an owner."""
        self.tasks = []
        for pet in owner.pets:
            self.tasks.extend(pet.tasks)

    def get_daily_tasks(self, date: datetime) -> List[Task]:
        """Return all daily tasks sorted chronologically by time and priority tier."""
        target_date = date.date()
        daily_tasks = [t for t in self.tasks if t.date_time.date() == target_date]
        daily_tasks.sort(key=lambda t: (t.date_time, -t.priority_value))
        return daily_tasks

    def generate_plan(self, date: datetime, max_available_minutes: int) -> Tuple[List[Task], List[Task]]:
        """Generate a structured daily schedule limited by overall duration minutes capacity."""
        all_daily = self.get_daily_tasks(date)
        scheduled, skipped = [], []
        total_time_used = 0

        for task in all_daily:
            if total_time_used + task.duration_minutes <= max_available_minutes:
                scheduled.append(task)
                total_time_used += task.duration_minutes
            else:
                skipped.append(task)
        return scheduled, skipped

    def detect_conflicts(self) -> List[Tuple[Task, Task]]:
        """Find overlapping target execution window windows for individual pets."""
        conflicts = []
        pet_tasks_map = {}
        for task in self.tasks:
            pet_tasks_map.setdefault(task.pet_name, []).append(task)

        for pet_name, tasks in pet_tasks_map.items():
            sorted_tasks = sorted(tasks, key=lambda t: t.date_time)
            for i in range(len(sorted_tasks)):
                for j in range(i + 1, len(sorted_tasks)):
                    t1, t2 = sorted_tasks[i], sorted_tasks[j]
                    if t1.date_time < t2.end_time and t2.date_time < t1.end_time:
                        conflicts.append((t1, t2))
        return conflicts
