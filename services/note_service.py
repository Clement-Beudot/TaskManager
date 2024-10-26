from objects.note import Note
from utils.json_utils import save_json

NOTES_FILE = "notes.json"

class NoteService:
    def __init__(self, notes_data=None):
        if isinstance(notes_data, dict) and "content" in notes_data:
            self.notes = notes_data["content"]
        elif isinstance(notes_data, str):
            self.notes = notes_data
        else:
            self.notes = ""

    def update_notes(self, new_content):
        """Update content quick note in Json file."""
        self.notes = new_content
        save_json(NOTES_FILE, {"content": self.notes})