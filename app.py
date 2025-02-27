from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.binding import Binding
from textual.widgets import Button, Input, Static, Footer, Select, ListView, ListItem, TextArea
from services.task_service import TaskService
from services.note_service import NoteService
from utils.json_utils import load_json, save_json
from utils.date_utils import to_string, to_date, today

TASKS_FILE = "tasks.json"
NOTES_FILE = "notes.json"

class TaskManagerApp(App):
    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("c", "open_create_task_dialog", "Add"),
        ("e", "open_update_task_dialog", "Edit task"),
        ("s", "open_dialog", "Change Status"),
        ("n", "toggle_notes", "Toggle Notes"), 
        Binding("ctrl+q", "app.quit", "Quit", show=True),
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.task_service = TaskService(load_json(TASKS_FILE, default_value=[]))
        self.note_service = NoteService(load_json(NOTES_FILE, default_value=""))
        self.tasks = self.task_service.tasks
        self.notes = self.note_service.notes

    def compose(self) -> ComposeResult:
        """Compose the user interface"""
        yield Container(Static("TaskManager"), id="header-container")
        
        self.task_list = ListView(id="tasks-list")
        yield self.task_list
        
        self.note_area = TextArea(self.note_service.notes, id="note-area")
        yield Container(self.note_area, id="note-container", classes="hidden")
        
        yield Footer()

    async def on_mount(self):
        """Called when the app is mounted"""
        await self.update_tasks_view()
        await self.update_header()

    async def update_tasks_view(self):
        while self.task_list.children:
            await self.task_list.children[0].remove()
        open_tasks = [task for task in self.tasks if task.status != "Done"]
        done_tasks = [task for task in self.tasks if task.status == "Done"]

        if open_tasks:
            self.task_list.append(ListItem(Static(f"Open Tasks [ {len(open_tasks)} ]"), classes="section-header"))
            for task in open_tasks:
                self._add_task_to_list(task)

        if done_tasks:
            self.task_list.append(ListItem(Static(f"Completed Tasks [ {len(done_tasks)} ]"), classes="section-header"))
            for task in done_tasks:
                self._add_task_to_list(task)

        await self.update_header()
        self.task_list.focus()

    def _add_task_to_list(self, task):
        """Add a task to Task List with it associated Id"""
        task_title = task.title
        task_due_date = to_string(task.due_date)
        task_status = task.status

        top_container = Horizontal(
            Static(task_title, classes="task-title"),
            Static(task.priority, classes=f"{task.priority.lower()}-priority"),
            classes="task-section-container"
        )
        bottom_container = Horizontal(
            Static(task_due_date, classes="task-due-date"),
            Static(task_status, classes="task-status"),
            classes="task-section-container"
        )
        task_item = Container(
            top_container,
            bottom_container,
            id=f"task-item-{task.id}" 
        )
        list_item = ListItem(task_item, id=f"task_id-{task.id}")
        self.task_list.append(list_item)

    async def update_header(self):
        """Update the header with task statistics"""
        stats = self.task_service.get_task_statistics()
        header_text = f"Open: {stats['open_tasks']} | Overdue: {stats['overdue_tasks']} | High/Urgent: {stats['high_priority_tasks']} | Risky: {stats['risky_tasks']}"
        header_container = self.query_one("#header-container")
        header_container.remove_children()
        await header_container.mount(Static(header_text))

    async def action_toggle_notes(self):
        """Toggle the visibility of the note-taking area"""
        note_container = self.query_one("#note-container")
        if "hidden" in note_container.classes:
            note_container.remove_class("hidden")
            self.note_area.focus()
        else:
            note_container.add_class("hidden")
            self.task_list.focus()

    async def on_text_area_changed(self, event: TextArea.Changed):
        """Save notes when they are modified"""
        if event.text_area.id == "note-area":
            self.note_service.update_notes(event.text_area.text)

    async def action_open_create_task_dialog(self):
        """Open the dialog to create a new task"""
        self.task_title_input = Input(placeholder="Enter task title")
        self.task_description_input = TextArea(id="task-description")
        self.task_priority_input = Select(options=[(priority, priority) for priority in ["Low", "Medium", "High", "Urgent"]], allow_blank=False)
        self.task_due_date_input = Input(placeholder="Due Date (dd-mm-yyyy)")
        self.database_action = "create"

        self.dialog = Container(
            Static("Create New Task"),
            self.task_title_input,
            self.task_description_input,
            self.task_priority_input,
            self.task_due_date_input,
            Horizontal(
                Button("Create Task", id="task-create-button"),
                Button("Cancel", id="dialog-cancel-button"),
            ),
            id="dialog",
        )
        await self.mount(self.dialog, before=self.query_one("#tasks-list"))
        self.task_title_input.focus()

    async def action_open_update_task_dialog(self):
        """Open panel to modify a selected task"""
        selected_item = self.task_list.index
        if selected_item is None:
            return
        task_item = self.task_list.children[selected_item]
        if not task_item.id or not task_item.id.startswith("task_id-"):
            return
        task_id = task_item.id.replace("task_id-", "")
        task = self.task_service.get_task_by_id(task_id)
        if not task:
            return
        self.task_title_input = Input(value=task.title)
        self.task_description_input = TextArea(task.description, id="task-description")
        self.task_status_input = Select(options=[(status, status) for status in ["To-do", "In progress", "Done", "Blocked"]], value=task.status, allow_blank=False)
        self.task_priority_input = Select(options=[(priority, priority) for priority in ["Low", "Medium", "High", "Urgent"]], value=task.priority, allow_blank=False)
        self.task_due_date_input = Input(value=to_string(task.due_date))
        self.database_action = "update"
        self.selected_task_id = task_id

        self.dialog = Container(
            Static(f"Edit {task.title}"),
            self.task_title_input,
            self.task_description_input,
            self.task_status_input,
            self.task_priority_input,
            self.task_due_date_input,
            Horizontal(
                Button("Update Task", id="task-update-button"),
                Button("Cancel", id="dialog-cancel-button"),
            ),
            id="dialog",
        )
        await self.mount(self.dialog, before=self.query_one("#tasks-list"))
        self.task_title_input.focus()

    async def on_button_pressed(self, event: Button.Pressed):
        """Handle actions when buttons are pressed"""
        button_id = event.button.id
        if button_id == "task-update-button" or button_id == "task-create-button":
            await self.handle_task_form_submission()

        elif button_id == "dialog-cancel-button":
            await self.dialog.remove()

    async def handle_task_form_submission(self):
        title = self.task_title_input.value.strip()
        priority = self.task_priority_input.value.strip()
        due_date = self.task_due_date_input.value.strip()
        description = self.task_description_input.text.strip()

        if title:
            if self.database_action == "create":
                self.task_service.create_task(
                    title = title, 
                    priority = priority, 
                    due_date = due_date, 
                    description = description
                )
            elif self.database_action == "update":
                self.task_service.update_task(
                    task_id = self.selected_task_id,
                    title = title, 
                    priority = priority, 
                    status = self.task_status_input.value, 
                    due_date = due_date,
                    description = description
                )
            await self.update_tasks_view()
        await self.dialog.remove()

    async def on_key(self, event):
        """Handle keyboard shortcuts, including hiding the note area"""
        if event.key == "escape":
            if self.note_area.has_focus:
                await self.action_toggle_notes()
            elif hasattr(self, "dialog"):
                await self.dialog.remove()
            if self.task_list:
                self.task_list.focus()
        if event.key == "enter":
            if hasattr(self, "dialog") and isinstance(self.focused, Input): 
                await self.handle_task_form_submission()
            #else: 
            #    await self.action_mark_task_done()

if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()