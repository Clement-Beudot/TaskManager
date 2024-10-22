from objects.note import Note
from utils.json_utils import save_json

NOTES_FILE = "notes.json"

class NoteService:
    def __init__(self, notes_data):
        self.notes = Note.from_dict({"content": notes_data})

    def update_notes(self, new_content):
        self.notes.update_content(new_content)
        self.save_notes()

    def save_notes(self):
        save_json(NOTES_FILE, {"content": self.notes.content})