from datetime import datetime
from utils.mapper.date_mapper import DATE_MAPPINGS

class Task:
    def __init__(self, title, priority, due_date, status="To-do"):
        self.title = title
        self.priority = priority
        self.due_date = due_date or DATE_MAPPINGS.get("tomorrow")
        self.status = status

    def is_overdue(self):
        if self.due_date:
            due_date = datetime.strptime(self.due_date, "%d-%m-%Y")
            return due_date < datetime.now()
        return False

    def mark_as_done(self):
        self.status = "Done"

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "due_date": self.due_date,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data["title"],
            priority=data["priority"],
            due_date=data["due_date"],
            status=data["status"]
        )