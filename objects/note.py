class Note:
    def __init__(self, content=""):
        self.content = content

    def update_content(self, new_content):
        self.content = new_content

    def to_dict(self):
        return {"content": self.content}

    @staticmethod
    def from_dict(data):
        return Note(
            content=data.get("content", "")
        )