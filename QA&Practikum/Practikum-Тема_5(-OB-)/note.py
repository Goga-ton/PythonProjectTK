import datetime

class Note:
    def __init__(self, title:str, content:str, created_at:datetime.datetime=None, note_id:int=None):
        self.id = note_id
        self.title = title
        self.content = content
        self.created_at = created_at or datetime.datetime.now()

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    def from_row(row):
        import datetime
        return Note(
            note_id=int(row[0]),
            title=row[1],
            content=row[2],
            created_at=datetime.datetime.fromisoformat(row[3]),
        )


