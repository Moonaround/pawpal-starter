from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

def run_demo():
    print("=============================================")
    print("🧠 PAWPAL+ LAYER 4 ALGORITHMIC VALIDATION 🧠")
    print("=============================================\n")

    owner = Owner("Jordan", "jordan@example.com")
    mochi = Pet("Mochi", "Dog", 2)
    owner.add_pet(mochi)

    today = datetime(2026, 5, 20)

    # 1. Add tasks COMPLETELY OUT OF ORDER to test chronological sorting
    print("📥 Adding tasks out of order...")
    task_late = Task("t_late", "Mochi", "Evening Brush", "Grooming", today + timedelta(hours=18), 20, "Low")
    task_early = Task("t_early", "Mochi", "Morning Walk", "Exercise", today + timedelta(hours=8), 30, "High", "Daily")
    task_mid = Task("t_mid", "Mochi", "Midday Feeding", "Lunch", today + timedelta(hours=12), 15, "Medium")

    mochi.add_task(task_late)
    mochi.add_task(task_early)
    mochi.add_task(task_mid)

    # 2. Add an overlapping task at 8:15 AM to trigger the conflict detection engine
    task_clash = Task("t_clash", "Mochi", "Medication Dose", "Give pill", today + timedelta(hours=8, minutes=15), 10, "High")
    mochi.add_task(task_clash)

    scheduler = Scheduler()
    scheduler.sync_tasks_from_owner(owner)

    # 3. Print sorted timeline results
    print("\n📋 SORTED DAILY TIMELINE VIEW:")
    for task in scheduler.get_daily_tasks(today):
        print(f"  [{task.date_time.strftime('%H:%M')}] {task.title} ({task.duration_minutes} min) - Priority: {task.priority}")

    # 4. Fire conflict checker algorithm
    print("\n🔍 RUNNING CONFLICT DETECTION...")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for t1, t2 in conflicts:
            print(f"  ⚠️ Warning: Overlap detected between '{t1.title}' and '{t2.title}' for {t1.pet_name}!")

    # 5. Process an automated recurrence event
    print("\n♻️ PROCESSING RECURRING TASK LOGIC...")
    print(f"  Completing task: '{task_early.title}' (Frequency: {task_early.frequency}, Date: {task_early.date_time.strftime('%Y-%m-%d')})")
    next_task = task_early.mark_complete()
    if next_task:
        mochi.add_task(next_task)
        print(f"  🎉 Automation triggered! Spawned next task: '{next_task.title}' for date: {next_task.date_time.strftime('%Y-%m-%d %H:%M')}")

    print("\n=============================================")

if __name__ == "__main__":
    run_demo()
