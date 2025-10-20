from app.user import User

class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, id, name,enrolled_course_ids):
        # TODO: Call the parent class's __init__ method using super().
        super().__init__(id, name)
        # TODO: Initialize an empty list called 'enrolled_course_ids' to store the IDs of courses.
        self.enrolled_course_ids = enrolled_course_ids or []

    def enroll_in(self, course_id):
        if course_id not in self.enrolled_course_ids:
            self.enrolled_course_ids.append(course_id)

