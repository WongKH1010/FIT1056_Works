from app.user import User

class StudentUser(User):
    """Represents a student."""
    def __init__(self, id, name, enrolled_in=None):
        super().__init__(id, name)
        self.enrolled_in = enrolled_in or []

    def enroll_in(self, instrument):
        if instrument not in self.enrolled_in:
            self.enrolled_in.append(instrument)

    def update_enrollment(self, new_enrollment):
        self.enrolled_in = new_enrollment   