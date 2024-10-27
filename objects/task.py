from utils.date_utils import to_string, to_date, today, max_at_risk_date
from uuid import uuid4

class Task:
    def __init__(self,
                title = "", 
                priority = "Low", 
                due_date = None, 
                description="", 
                status="To-do",
                task_id=None
                ):
        self.id = task_id or str(uuid4()) 
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = to_date(due_date)
        self.status = status

    def is_overdue(self):
        if self.due_date:
            return to_date(self.due_date) < today()
        return False
    
    def is_at_risk(self):
        if self.due_date:
            return (to_date(self.due_date) < max_at_risk_date() and to_date(self.due_date) >= today())
        return False

    def mark_as_done(self):
        self.status = "Done"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": to_string(self.due_date),
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            task_id=data["id"],
            title = data["title"],
            description = data.get("description", ""),
            priority = data["priority"],
            due_date = to_date(data["due_date"]),
            status = data["status"]
        )