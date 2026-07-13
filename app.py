import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Scheduler, save_system_data, load_system_data

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- CUSTOM HOOK FOR TASK EMOJI FORMATTING (CHALLENGE 4) ---
def get_task_emoji(title: str) -> str:
    title_lower = title.lower()
    if "walk" in title_lower or "exercise" in title_lower:
        return "🦮"
    if "feed" in title_lower or "food" in title_lower or "breakfast" in title_lower or "dinner" in title_lower:
        return "🥣"
    if "med" in title_lower or "pill" in title_lower or "vet" in title_lower:
        return "💊"
    if "groom" in title_lower or "brush" in title_lower or "bath" in title_lower:
        return "🧼"
    return "📝"

# Initialize state from our persistent storage layer file
if "owner" not in st.session_state:
    st.session_state["owner"] = load_system_data()

if "scheduler" not in st.session_state:
    st.session_state["scheduler"] = Scheduler()

owner = st.session_state["owner"]
scheduler = st.session_state["scheduler"]

st.title("🐾 PawPal+ Care Hub")

st.subheader("Profile Configuration")
ui_owner_name = st.text_input("Owner name", value=owner.name)
if ui_owner_name != owner.name:
    owner.name = ui_owner_name
    save_system_data(owner)

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

active_pet = next((p for p in owner.pets if p.name == pet_name), None)
if active_pet is None:
    active_pet = Pet(name=pet_name, species=species, age=2)
    owner.add_pet(active_pet)
    save_system_data(owner)

st.markdown("### Tasks")
col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if task_title:
        base_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=8)
        offset_minutes = sum(t.duration_minutes for t in active_pet.tasks)
        scheduled_dt = base_time + timedelta(minutes=offset_minutes)
        
        new_task = Task(
            task_id=f"task_{int(datetime.now().timestamp())}",
            pet_name=active_pet.name,
            title=task_title,
            description=f"Routine care",
            date_time=scheduled_dt,
            duration_minutes=int(duration),
            priority=priority.capitalize()
        )
        active_pet.add_task(new_task)
        save_system_data(owner)  # Save changes instantly to JSON database
        st.success(f"Added '{task_title}' successfully!")

if active_pet.tasks:
    st.write(f"Current tasks for **{active_pet.name}**:")
    display_list = [{"Emoji": get_task_emoji(t.title), "Title": t.title, "Duration (m)": t.duration_minutes, "Priority": t.priority} for t in active_pet.tasks]
    st.table(display_list)

st.divider()
st.subheader("Build Schedule")
max_time_allowed = st.slider("Max Available Time Capacity (minutes)", min_value=10, max_value=480, value=120)

if st.button("Generate schedule"):
    scheduler.sync_tasks_from_owner(owner)
    target_date = datetime.combine(datetime.today(), datetime.min.time())
    scheduled, skipped = scheduler.generate_plan(target_date, max_time_allowed)
    
    if not scheduled and not skipped:
        st.warning("No tasks found.")
    else:
        st.markdown(f"### Daily plan for {active_pet.name}:")
        for task in scheduled:
            time_str = task.date_time.strftime("%H:%M")
            emoji = get_task_emoji(task.title)
            # Use color-coded priority badges
            badge_color = "green" if task.priority == "Low" else "orange" if task.priority == "Medium" else "red"
            st.markdown(f"🔹 **{time_str}** — {emoji} **{task.title}** ({task.duration_minutes} min) :broken_heart:[<span style='color:{badge_color}'>{task.priority}</span>]", unsafe_allow_html=True)
            
        if skipped:
            st.markdown("---")
            st.markdown("⚠️ **Omitted due to limits:**")
            for task in skipped:
                st.markdown(f"🔸 ~~{task.title}~~ ({task.duration_minutes} min)")

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.error("⚠️ **Schedule Time Conflicts Detected!**")
