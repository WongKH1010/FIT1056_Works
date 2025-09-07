class Course:
    """Represents a music course."""
    def __init__(self, course_id, name, instrument, teacher_id):
        self.id = course_id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        self.enrolled_student_ids = []
        self.lessons = []

    def enroll_student(self, student_id):
        if student_id not in self.enrolled_student_ids:
            self.enrolled_student_ids.append(student_id)

    def remove_student(self, student_id):
        if student_id in self.enrolled_student_ids:
            self.enrolled_student_ids.remove(student_id)