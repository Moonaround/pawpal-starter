import streamlit as st
from datetime import datetime, timedelta
# --- STEP 1: ESTABLISH THE CONNECTION ---
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- STEP 2: MANAGE THE APPLICATION MEMORY ---
if "owner" not in st.session_state:
    # Initialize the core owner profile in the session memory vault
    st.session_state["owner"] = Owner("Jordan", "jordan@example.com")

if "scheduler" not in st.session_state:
    # Initialize the central scheduling system brain
    st.session_state["scheduler"] = Scheduler()

# Pull our active objects from session state to keep data stable across clicks
owner = st.session_state["owner"]
scheduler = st.session_state["scheduler"]

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ application. Your modular object-oriented backend logic layer 
is now fully integrated with this user interface.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

st.subheader("Profile Configuration")
# Allow the user to update the active owner profile configuration dynamically
ui_owner_name = st.text_input("Owner name", value=owner.name)
owner.name = ui_owner_name

# Sync our default pet into the backend if it isn't tracked yet
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Check if this pet is already in the backend; if not, create it
active_pet = None
for p in owner.pets:
    if p.name == pet_name:
        active_pet = p
        break

if active_pet is None:
    active_pet = Pet(name=pet_name, species=species, age=2)
    owner.add_pet(active_pet)

st.markdown("### Tasks")
st.caption("Add care routine tasks below. These tasks feed directly into your algorithmic scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# --- STEP 3: WIRING UI ACTIONS TO LOGIC ---
if st.button("Add task"):
    if task_title:
        # Create a timestamp starting today at 8:00 AM, offsetting tasks incrementally
        base_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=8)
        offset_minutes = sum(t.duration_minutes for t in active_pet.tasks)
        scheduled_dt = base_time + timedelta(minutes=offset_minutes)
        
        # Instantiate a formal backend Task object
        new_task = Task(
            task_id=f"task_{int(datetime.now().timestamp())}_{len(active_pet.tasks)}",
            pet_name=active_pet.name,
            title=task_title,
            description=f"Routine care for {active_pet.name}",
            date_time=scheduled_dt,
            duration_minutes=int(duration),
            priority=priority.capitalize()  # Standardize to High, Medium, Low
        )
        
        # Wire action directly to the pet backend method
        active_pet.add_task(new_task)
        st.success(f"Added '{task_title}' to {active_pet.name}'s task profile!")
    else:
        st.error("Please enter a valid task title.")

# Render live tasks from the actual backend object data structures
if active_pet.tasks:
    st.write(f"Current backend tasks for **{active_pet.name}**:")
    display_list = []
    for t in active_pet.tasks:
        display_list.append({
            "Title": t.title,
            "Duration (m)": t.duration_minutes,
            "Priority": t.priority
        })
    st.table(display_list)
else:
    st.info("No tasks registered yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Configure available schedule constraints to test filtration algorithms.")

# Add a constraint slider to limit schedule generation time windows
max_time_allowed = st.slider("Max Available Time Capacity (minutes)", min_value=10, max_value=480, value=120, step=10)

if st.button("Generate schedule"):
    # Synchronize and aggregate recent updates into the scheduler container
    scheduler.sync_tasks_from_owner(owner)
    
    # Run optimization plan logic based on active date timeline
    target_date = datetime.combine(datetime.today(), datetime.min.time())
    scheduled, skipped = scheduler.generate_plan(target_date, max_time_allowed)
    
    if not scheduled and not skipped:
        st.warning("No tasks found to schedule. Add tasks above first!")
    else:
        st.success("🗓️ Daily Optimized Plan Generated successfully!")
        
        st.markdown(f"### Daily plan for {active_pet.name} ({active_pet.species}):")
        for task in scheduled:
            time_str = task.date_time.strftime("%H:%M")
            st.markdown(f"🔹 **{time_str}** — {task.title} ({task.duration_minutes} min) `[priority: {task.priority.lower()}]`")
            
        # Explaining the logic / reasoning engine results transparently to the user
        st.info(f"💡 **Scheduler Reasoning:** Tasks were ordered chronologically. "
                f"A total of {sum(t.duration_minutes for t in scheduled)} minutes of care was scheduled.")
        
        if skipped:
            st.markdown("---")
            st.markdown("⚠️ **Omitted Tasks (Exceeded Time Capacity Constraints):**")
            for task in skipped:
                st.markdown(f"🔸 ~~{task.title}~~ ({task.duration_minutes} min) — *Dropped to preserve available time limits.*")

        # Conflict Handling checks
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.error("⚠️ **Schedule Time Conflicts Detected!** Multi-task overlap identified for the same asset.")
