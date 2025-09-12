class Course:
    """Represents a music course."""
    def __init__(self, id, name, instrument, teacher_id,enrolled_student_ids,lessons):
        self.id = id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        self.enrolled_student_ids = enrolled_student_ids or []
        self.lessons = lessons or []

    def enroll_student(self, student_id):
        if student_id not in self.enrolled_student_ids:
            self.enrolled_student_ids.append(student_id)

    def remove_student(self, student_id):
        if student_id in self.enrolled_student_ids:
            self.enrolled_student_ids.remove(student_id)