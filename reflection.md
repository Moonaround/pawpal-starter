# PawPal+ Project Reflection

# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
The initial system architecture is structured around four primary modular classes to handle clean object interactions:
- **Owner**: Manages user details and stores registered pet instances.
- **Pet**: Uses a clean Python Dataclass structure to manage animal characteristics like name, species, age, and health history.
- **Task**: Represents care requirements (feedings, walks) containing a definitive start time, duration, and priority level.
- **Scheduler**: Operates as the central logic runner to execute task chronological sorting, total duration constraints, and overlap checking.

**b. Design changes**
During the initial UML setup, the `Pet` and `Task` structures were moved from standard classes to modern Python Dataclasses. This architectural choice automatically implements the `__init__` constructor method, ensuring simpler data object tracking and lower code complexity.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**
The conflict detection algorithm uses an O(N²) nested inspection loop to evaluate calendar events. While this design is slightly less efficient for massive databases, it is highly reasonable here because individual pet profiles rarely exceed 10–15 scheduled routine care items a day, allowing the code to remain simple, legible, and lightweight.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**
I implemented automated test suites targeting bounding criteria: chronological sequencing arrays, overlapping timeline checking vectors, time duration capacity filtration caps, and recursive daily generation objects. These tests guarantee that core scheduling calculations run accurately behind the scenes.

**b. Confidence**
I rate system operational reliability as a 5/5. If given more time, I would build test vectors checking year-boundary transition math (e.g., Leap Years or Daylight Savings switches) to protect time metrics globally.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
