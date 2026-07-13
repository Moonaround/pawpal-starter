import json
import os
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
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
    frequency: str = "Once"  # "Once", "Daily", "Weekly"
    is_completed: bool = False

    def mark_complete(self) -> Optional['Task']:
        """Mark the task as completed and handle recurrence."""
        self.is_completed = True
        if self.frequency == "Daily":
            return Task(f"{self.task_id}_next", self.pet_name, self.title, self.description, self.date_time + timedelta(days=1), self.duration_minutes, self.priority, self.frequency)
        elif self.frequency == "Weekly":
            return Task(f"{self.task_id}_next", self.pet_name, self.title, self.description, self.date_time + timedelta(weeks=1), self.duration_minutes, self.priority, self.frequency)
        return None

    @property
    def end_time(self) -> datetime:
        return self.date_time + timedelta(minutes=self.duration_minutes)

    @property
    def priority_value(self) -> int:
        mapping = {"High": 3, "Medium": 2, "Low": 1}
        return mapping.get(self.priority, 0)

    def to_dict(self) -> dict:
        """Convert a Task instance into a JSON-serializable dictionary."""
        return {
            "task_id": self.task_id, "pet_name": self.pet_name, "title": self.title,
            "description": self.description, "date_time": self.date_time.isoformat(),
            "duration_minutes": self.duration_minutes, "priority": self.priority,
            "frequency": self.frequency, "is_completed": self.is_completed
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'Task':
        """Reconstruct a Task instance from a dictionary."""
        return cls(
            task_id=d["task_id"], pet_name=d["pet_name"], title=d["title"],
            description=d["description"], date_time=datetime.fromisoformat(d["date_time"]),
            duration_minutes=d["duration_minutes"], priority=d["priority"],
            frequency=d.get("frequency", "Once"), is_completed=d["is_completed"]
        )

@dataclass
class Pet:
    name: str
    species: str
    age: int
    medical_notes: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def to_dict(self) -> dict:
        return {
            "name": self.name, "species": self.species, "age": self.age,
            "medical_notes": self.medical_notes, "tasks": [t.to_dict() for t in self.tasks]
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'Pet':
        pet = cls(name=d["name"], species=d["species"], age=d["age"], medical_notes=d["medical_notes"])
        pet.tasks = [Task.from_dict(t) for t in d.get("tasks", [])]
        return pet

class Owner:
    def __init__(self, name: str, email: str):
        self.name: str = name
        self.email: str = email
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        if not any(p.name == pet.name for p in self.pets):
            self.pets.append(pet)

    def to_dict(self) -> dict:
        return {"name": self.name, "email": self.email, "pets": [p.to_dict() for p in self.pets]}

    @classmethod
    def from_dict(cls, d: dict) -> 'Owner':
        owner = cls(name=d["name"], email=d["email"])
        owner.pets = [Pet.from_dict(p) for p in d.get("pets", [])]
        return owner

class Scheduler:
    def __init__(self):
        self.tasks: List[Task] = []

    def sync_tasks_from_owner(self, owner: Owner) -> None:
        self.tasks = []
        for pet in owner.pets:
            self.tasks.extend(pet.tasks)

    def get_daily_tasks(self, date: datetime) -> List[Task]:
        target_date = date.date()
        daily_tasks = [t for t in self.tasks if t.date_time.date() == target_date]
        daily_tasks.sort(key=lambda t: (t.date_time, -t.priority_value))
        return daily_tasks

    def generate_plan(self, date: datetime, max_available_minutes: int) -> Tuple[List[Task], List[Task]]:
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
        conflicts = []
        pet_tasks_map = {}
        for task in self.tasks:
            if not task.is_completed:
                pet_tasks_map.setdefault(task.pet_name, []).append(task)
        for pet_name, tasks in pet_tasks_map.items():
            sorted_tasks = sorted(tasks, key=lambda t: t.date_time)
            for i in range(len(sorted_tasks)):
                for j in range(i + 1, len(sorted_tasks)):
                    t1, t2 = sorted_tasks[i], sorted_tasks[j]
                    if t1.date_time < t2.end_time and t2.date_time < t1.end_time:
                        conflicts.append((t1, t2))
        return conflicts

# --- GLOBAL UTILITIES FOR JSON DATA PERSISTENCE ---
DB_FILE = "data.json"

def save_system_data(owner: Owner) -> None:
    """Save the full owner profile state out to a storage file."""
    with open(DB_FILE, "w") as f:
        json.dump(owner.to_dict(), f, indent=4)

def load_system_data() -> Owner:
    """Load system data or fallback to a standard initial profile framework."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return Owner.from_dict(json.load(f))
        except Exception:
            pass
    return Owner("Jordan", "jordan@example.com")
