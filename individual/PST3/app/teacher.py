from app.user import User

class TeacherUser(User):
    """Represents a teacher."""
    def __init__(self, id, name, specialty):
        super().__init__(id, name)
        self.specialty = specialty

    def update_specialty(self, new_specialty):
        self.specialty = new_specialty
