from objects.task import Task
from utils.json_utils import save_json
from utils.mapper.date_mapper import DATE_MAPPINGS
from datetime import datetime

TASKS_FILE = "tasks.json"

class TaskService:
    def __init__(self, tasks_data):
        self.tasks = [Task.from_dict(task) for task in tasks_data]

    def get_all_tasks(self):
        return self.tasks
    
    def get_task_by_index(self, index):
        """Return the task that by his index in task-list"""
        if index < 0 or index >= len(self.tasks):
            raise IndexError("Index is out of bound")
        return self.tasks[index]

    def get_task_statistics(self):
        open_tasks = [task for task in self.tasks if task.status != "Done"]
        overdue_tasks = [task for task in open_tasks if task.is_overdue()]
        high_priority_tasks = [task for task in open_tasks if task.priority in ["High", "Urgent"]]
        risky_tasks = [task for task in open_tasks if task.is_overdue()]
        return {
            "open_tasks": len(open_tasks),
            "overdue_tasks": len(overdue_tasks),
            "high_priority_tasks": len(high_priority_tasks),
            "risky_tasks": len(risky_tasks),
        }


    def create_task(self, title, priority, due_date):
        new_task = Task(title, priority, self.process_due_date(due_date))
        self.tasks.append(new_task)
        self.save_tasks()

    def update_task(self, index, title=None, priority=None, status=None, due_date=None):
        """Update an existing task"""
        if index < 0 or index >= len(self.tasks):
            raise IndexError("Tax Index is out of bound")
        
        task = self.tasks[index]
        if title:
            task.title = title
        if priority:
            task.priority = priority
        if status:
            task.status = status
        if due_date:
            task.due_date = self.process_due_date(due_date)

        self.save_tasks()

    def save_tasks(self):
        tasks_data = [task.to_dict() for task in self.tasks]
        save_json(TASKS_FILE, tasks_data)

    def match_input_to_date(self, input_text):
        input_text = input_text.lower()
        for key in DATE_MAPPINGS:
            if input_text != "" and key.startswith(input_text):
                return DATE_MAPPINGS[key]
        return None
    
    def get_default_due_date(self):
        return datetime.now().strftime("%d-%m-%Y")
    
    def is_valid_date(self, date_str):
        if not date_str: 
            return False
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False
        
    def process_due_date(self, due_date=None):
        if due_date and self.is_valid_date(due_date):
            return due_date
        return self.match_input_to_date(due_date) if self.match_input_to_date(due_date) else self.get_default_due_date()
