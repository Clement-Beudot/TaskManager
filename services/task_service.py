from objects.task import Task
from utils.json_utils import save_json
from utils.mapper.date_mapper import DATE_MAPPINGS
from utils.date_utils import to_string, to_date, today
from datetime import datetime

TASKS_FILE = "tasks.json"

class TaskService:
    def __init__(self, tasks_data):
        self.tasks = [Task.from_dict(task) for task in tasks_data]

    def get_all_tasks(self):
        return self.tasks
    
    def get_task_by_id(self, task_id):
        """Get a task by Id"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_task_statistics(self):
        open_tasks = [task for task in self.tasks if task.status != "Done"]
        overdue_tasks = [task for task in open_tasks if task.is_overdue()]
        high_priority_tasks = [task for task in open_tasks if task.priority in ["High", "Urgent"]]
        risky_tasks = [task for task in open_tasks if task.is_at_risk()]
        return {
            "open_tasks": len(open_tasks),
            "overdue_tasks": len(overdue_tasks),
            "high_priority_tasks": len(high_priority_tasks),
            "risky_tasks": len(risky_tasks),
        }


    def create_task(self, title, priority, due_date, description=""):
        new_task = Task(title, priority, self.process_due_date(due_date), description)
        self.tasks.append(new_task)
        self.save_tasks()

    def update_task(self, task_id, title=None, priority=None, status=None, due_date=None, description=None):
        """Update an existing task"""
        task = self.get_task_by_id(task_id)
        
        if task :
            if title:
                task.title = title
            if priority:
                task.priority = priority
            if status:
                task.status = status
            if due_date:
                task.due_date = self.process_due_date(due_date)
            if description:
                task.description = description
            self.save_tasks()

    def save_tasks(self):
        tasks_data = [task.to_dict() for task in self.tasks]
        save_json(TASKS_FILE, tasks_data)

    def match_input_to_date(self, input_text):
        input_text = input_text.lower()
        for key in DATE_MAPPINGS:
            if input_text != "" and key.startswith(input_text):
                return to_date(DATE_MAPPINGS[key])
        return None
    
    def get_default_due_date(self):
        return today()
    
    def is_valid_date(self, date_str):
        if not date_str: 
            return False
        return to_date(date_str) is not None
        
    def process_due_date(self, due_date=None):
        if isinstance(due_date, datetime):
            return due_date
        elif isinstance(due_date, str) and self.is_valid_date(due_date):
            return to_date(due_date)
        elif isinstance(due_date, str):
            mapped_date = self.match_input_to_date(due_date)
            if mapped_date:
                return mapped_date
        return self.get_default_due_date()