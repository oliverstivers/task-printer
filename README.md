# Task-Printer: Hybrid Physical-Digital Task Management System

## Overview
The task-printer system is a hybrid physical-digital task management application. Each active (non-done) task is associated with a unique AprilTag ID, allowing status updates through physical scanning via camera. Tasks can be created digitally via CLI, printed with embedded AprilTags, and their status changed by moving printed cards between zones (TODO, DOING, DONE). The system supports task hierarchies, integrates with Google Calendar for scheduling, uses AI for task recommendations, and scrapes course websites for assignments.

Designed for AI agents: This README provides structured information for automation, including code snippets, API-like interactions, and programmable interfaces.

## Key Features
- **Task Lifecycle**: Create tasks via CLI, print with AprilTags, scan via camera to update status.
- **Hierarchies**: Parent/child task relationships using treelib for visualization.
- **Integrations**: Google Calendar for event fetching, OpenAI for AI recommendations, web scraping for assignments.
- **Persistence**: File-based storage using pickle (tasks.pkl, tagmap.pkl, categories.pkl).
- **Physical Interaction**: Real-time AprilTag detection with zone-based status updates.

## Architecture & Data Flow
- **Modular Components**: Task class, TaskManager (global state), Scanner (vision), Printer (queue), Client (CLI), integrations.
- **Data Flow**:
  1. CLI creation → Task instantiation → Assign AprilTag ID.
  2. Add to print queue → Generate image with AprilTag → Save for printing.
  3. Physical scanning → Detect tag position → Update status in TaskManager.
  4. Persistence: Save/load via pickle files.
- **External Dependencies**: OpenCV (vision), PIL (images), pupil_apriltags (detection), requests/BeautifulSoup (scraping), openai (AI), prompt_toolkit (CLI).

## Component Breakdown
### Task (task.py)
- **Purpose**: Represents individual tasks with attributes like name, due_date, category, status, parent_id, april_tag_id.
- **Key Methods**:
  - `generate_image()`: Creates 384px-wide printable image with task details and AprilTag.
  - `receipt()`: Returns text summary for CLI display.
  - `update_status(status)`: Changes status and updates print_time if needed.
- **Example for AI Agents**:
  ```python
  from task import Task
  task = Task(name="Review PR", due_date="2024-01-15", category="work")
  image_path = task.generate_image()
  print(task.receipt())
  ```

### TaskManager (task_manager.py)
- **Purpose**: Manages global tasks list, tag mappings, and persistence.
- **Key Methods**:
  - `add_task(task)`: Adds task, assigns tag if active.
  - `load_tasks()`: Deserializes from tasks.pkl.
  - `save_tasks()`: Serializes tasks to files.
  - `get_task_by_tag(tag_id)`: Retrieves task by AprilTag ID.
- **Example**:
  ```python
  from task_manager import TaskManager
  tm = TaskManager()
  tm.load_tasks()
  task = tm.get_task_by_tag(42)
  tm.save_tasks()
  ```

### Scanner (scanner.py)
- **Purpose**: Real-time AprilTag detection via camera, updates status based on zones.
- **Key Logic**: Divides view into TODO (left), DOING (middle), DONE (right); tracks scanned_ids.json to avoid duplicates.
- **Example Interaction**: Agents can run scanner loop in background; status updates trigger callbacks.

### Printer (printer.py)
- **Purpose**: Manages print queue; processes tasks for image generation (stubs for hardware).
- **Key Methods**:
  - `add_to_queue(task)`: Queues task for printing.
  - `process_queue()`: Generates and saves images.
- **Example**:
  ```python
  from printer import Printer
  printer = Printer()
  printer.add_to_queue(task)
  printer.process_queue()
  ```

### Client (client.py)
- **Purpose**: CLI interface for user interaction.
- **Key Features**: Add tasks with auto-completion, view tasks, recommend from calendar.
- **Example Commands**: `python client.py --add "New Task" --due 2024-01-20 --category work`

### Integrations
- **Google Calendar (gcal_quickstart.py)**: Fetches events; example: `get_calendar_events(days=4)`
- **OpenAI**: Recommends tasks; assumes localhost:8080 endpoint.
- **Scraper (scrape.py)**: Scrapes assignments; hardcoded for specific courses.

## Usage for AI Agents
- **Task Creation**: Use Client or TaskManager directly to instantiate and persist tasks.
- **Scanning Automation**: Run Scanner in thread; monitor status changes for triggers.
- **Integrations**: Fetch calendar events, generate AI recommendations, scrape data.
- **Persistence Access**: Read/write pickle files for state management.
- **Example Workflow**:
  1. Load tasks: `tm.load_tasks()`
  2. Create task: `task = Task(...)`
  3. Assign tag: `tm.add_task(task)`
  4. Print: `printer.add_to_queue(task)`
  5. Scan: Run scanner to update status.

## Installation & Setup
- **Dependencies**: Install via `pip install -r requirements.txt` (includes opencv-python, pillow, etc.).
- **Setup**:
  - Google Calendar: Set up OAuth (credentials.json, token.json).
  - OpenAI: Run local instance on :8080.
  - Camera: Ensure permissions for OpenCV.
- **Environment**: Python 3.x; assumes thermal printer for physical printing (currently image-only).

## Limitations & Best Practices
- **Incompleteness**: Printing is image generation only (no hardware interface). Scraper is course-specific. No database.
- **Security**: Store OAuth tokens securely; use local OpenAI for privacy.
- **Code Style**: Follow AGENTS.md: 4-space indentation, type hints, absolute imports, sorted categories.
- **Extensions**: Add GUI, database, mobile scanning; handle errors for missing tags.
- **Performance**: Pickle for small-scale; consider JSON for larger datasets.

## API Reference
- **Task**: `__init__(name, due_date=None, category='', status='TODO', duration=None, recurrence=None, parent_id=None)`
- **TaskManager**: `load_tasks()`, `save_tasks()`, `add_task(task)`, `get_task_by_tag(tag_id)`
- **Printer**: `add_to_queue(task)`, `process_queue()`
- **Scanner**: Run via `scanner.py` (no class API; procedural).
- **Client**: CLI entry; use `python client.py [options]`

For AI agents, focus on programmatic access via classes for automation and integration. 
 