from app.user import User

class TeacherUser(User):
    """Represents a teacher."""
    # TODO: Implement the TeacherUser class, inheriting from User.
    # It should have an additional 'speciality' attribute in its __init__.
    def __init__(self, id, name, speciality):
        super().__init__(id, name)
        self.speciality = speciality

class Course:
    """Represents a single course offered by the school, linked to a teacher."""
    def __init__(self, id, name, instrument, teacher_id,enrolled_student_ids,lessons,fees):
        self.id = id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        self.fees = fees
        # TODO: Initialize two empty lists: 'enrolled_student_ids' and 'lessons'.
        self.enrolled_student_ids = enrolled_student_ids or []
        self.lessons = lessons or [] # This will hold lesson dictionaries
    
    def enroll_student(self, student_id):
        if student_id not in self.enrolled_student_ids:
            self.enrolled_student_ids.append(student_id)
    
    def remove_student(self, student_id):
        if student_id not in self.enrolled_student_ids:
            self.enrolled_student_ids.remove(student_id)