from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

def run_demo():
    print("=============================================")
    print("🐾 PAWPAL+ SYSTEM CORE CLI TESTING GROUND 🐾")
    print("=============================================\n")

    # 1. Create an Owner and Pets
    owner = Owner("Jap", "jap@example.com")
    biscuit = Pet("Biscuit", "Golden Retriever", 3)
    luna = Pet("Luna", "Cat", 2)
    
    owner.add_pet(biscuit)
    owner.add_pet(luna)
    print(f"✅ Registered Owner: {owner.name}")
    print(f"🐶 Added Pets: {biscuit.name} ({biscuit.species}), {luna.name} ({luna.species})\n")

    # 2. Add Tasks with different chronological times
    today = datetime(2026, 5, 20)
    
    # Task A: 8:00 AM
    task1 = Task("t1", "Biscuit", "Morning Walk", "Exercise around park", today + timedelta(hours=8), 30, "High")
    # Task B: 9:00 AM
    task2 = Task("t2", "Biscuit", "Breakfast Feeding", "Kibble and meds", today + timedelta(hours=9), 15, "High")
    # Task C: 2:00 PM (14:00)
    task3 = Task("t3", "Luna", "Grooming Session", "Brush loose fur", today + timedelta(hours=14), 20, "Medium")

    biscuit.add_task(task1)
    biscuit.add_task(task2)
    luna.add_task(task3)

    # 3. Use the central Scheduler brain
    scheduler = Scheduler()
    scheduler.sync_tasks_from_owner(owner)
    
    # 4. Print Today's Plan beautifully to the terminal
    print("📋 DAILY PLAN GENERATED:")
    daily_plan = scheduler.get_daily_tasks(today)
    
    for task in daily_plan:
        time_str = task.date_time.strftime("%H:%M")
        print(f"  {time_str} — {task.title} for {task.pet_name} ({task.duration_minutes} min) [priority: {task.priority.lower()}]")
    
    print("\n=============================================")

if __name__ == "__main__":
    run_demo()
