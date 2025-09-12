import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser
from app.course import Course

class SchoolManager:
    """Main controller for all MSMS operations."""
    ADMIN_PASSWORD = "1234567"
    STUDENT_PASSWORD = "7654321"

    def __init__(self, data_path="individual/PST3/data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.next_student_id = 1
        self.next_teacher_id = 1
        self._load_data()

    # --- Persistence ---
    def _load_data(self):
        try:
            with open(self.data_path, "r") as f:
                data = json.load(f)
                self.teachers = [TeacherUser(**t) for t in data.get("teachers", [])]
                self.students = [StudentUser(**s) for s in data.get("students", [])]
                self.courses = [Course(**c) for c in data.get("courses", [])]
                self.attendance_log = data.get("attendance", [])
                self.next_student_id = data.get("next_student_id", 1)
                self.next_teacher_id = data.get("next_teacher_id", 1)
        except FileNotFoundError:
            print("Data file not found. Starting new database.")

    def _save_data(self):
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            "attendance": self.attendance_log,
            "next_student_id": self.next_student_id,
            "next_teacher_id": self.next_teacher_id
        }
        with open(self.data_path, "w") as f:
            json.dump(data_to_save, f, indent=4)

    # --- User Management ---
    def add_student(self, name, instrument):
        student = StudentUser(self.next_student_id, name, [instrument])
        self.students.append(student)
        self.next_student_id += 1
        self._save_data()
        print(f"Added Student {name}, ID: {student.id}")

    def add_teacher(self, name, specialty):
        teacher = TeacherUser(self.next_teacher_id, name, specialty)
        self.teachers.append(teacher)
        self.next_teacher_id += 1
        self._save_data()
        print(f"Added Teacher {name}, ID: {teacher.id}")

    def remove_student(self, student_id):
        student = self.find_student(student_id)
        if student:
            self.students.remove(student)
            self._save_data()
            print(f"Student {student_id} removed")
        else:
            print("Student not found")

    def remove_teacher(self, teacher_id):
        teacher = self.find_teacher(teacher_id)
        if teacher:
            self.teachers.remove(teacher)
            self._save_data()
            print(f"Teacher {teacher_id} removed")
        else:
            print("Teacher not found")
            

    # --- Unified Search ---
    def find_student(self, term):
        for s in self.students:
            if str(s.id) == str(term) or term.lower() in s.name.lower():
                return s
        return None

    def find_teacher(self, term):
        for t in self.teachers:
            if str(t.id) == str(term) or term.lower() in t.name.lower():
                return t
        return None
    
    def find_course_by_id(self,course_to_find):
        for course in self.courses:
            if str(course.id) == str(course_to_find):
                return course

    # --- Courses ---
    def add_course(self, name, instrument, teacher_id):
        teacher = self.find_teacher(teacher_id)
        if not teacher:
            print("Teacher not found")
            return
        course_id = max([c.id for c in self.courses], default=100) + 1
        course = Course(course_id, name, instrument, teacher_id)
        self.courses.append(course)
        self._save_data()
        print(f"Added Course {name} ID: {course_id}")
    
    def add_lesson_to_course(self, course_id, day, start_time, room):
        """Admin-only: Adds a lesson to a course."""
        course = self.find_course_by_id(course_id)
        if not course:
            print(f"Error: Course ID {course_id} not found.")
            return False

        # Auto-generate lesson_id based on existing lessons
        lesson_id = 1
        if course.lessons:
            lesson_id = max(l['lesson_id'] for l in course.lessons) + 1

        lesson = {
            "lesson_id": lesson_id,
            "day": day,
            "start_time": start_time,
            "room": room
        }

        course.lessons.append(lesson)
        self._save_data()
        print(f"Lesson added to {course.name}: {day} at {start_time} in {room}.")
        return True

    def enroll_student_in_course(self, student_id, course_id):
        student = self.find_student(student_id)
        course = self.find_course_by_id(course_id)
        if student and course:
            student.enroll_in(course.instrument)
            course.enroll_student(student.id)
            self._save_data()
            print(f"Enrolled {student.name} in {course.name}")
        else:
            print("Invalid student or course")

    def switch_student_course(self, student_id, from_course_id, to_course_id):
        student = self.find_student(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not all([student, from_course, to_course]):
            print("Invalid IDs provided")
            return

        if from_course_id not in student.enrolled_in:
            print("Student not enrolled in from_course")
            return

        if to_course_id in student.enrolled_in:
            print("Student already enrolled in target course")
            return

        student.enrolled_in.remove(from_course.instrument)
        student.enrolled_in.append(to_course.instrument)
        from_course.remove_student(student_id)
        to_course.enroll_student(student_id)
        self._save_data()
        print(f"{student.name} switched from {from_course.name} to {to_course.name}")

    # --- Attendance ---
    def check_in(self, student_id, course_id):
        student = self.find_student(student_id)
        course = self.find_course_by_id(course_id)
        if student and course:
            self.attendance_log.append({
                "student_id": student_id,
                "course_id": course_id,
                "timestamp": datetime.datetime.now().isoformat()
            })
            self._save_data()
            print(f"Checked in {student.name} to {course.name}")
        else:
            print("Invalid student or course ID")

    # --- Listing ---
    def list_students(self):
        for s in self.students:
            print(f"{s.id}: {s.name} Enrolled in {s.enrolled_in}")

    def list_teachers(self):
        for t in self.teachers:
            print(f"{t.id}: {t.name} Specialty {t.specialty}")

    # --- Student Card ---
    def print_student_card(self, student_id):
        student = self.find_student(student_id)
        if student:
            filename = f"{student.id}_card.txt"
            with open(filename, "w") as f:
                f.write("========================\n")
                f.write("  MUSIC SCHOOL ID BADGE\n")
                f.write("========================\n")
                f.write(f"ID: {student.id}\n")
                f.write(f"Name: {student.name}\n")
                f.write(f"Enrolled In: {', '.join(student.enrolled_in)}\n")
            print(f"Student card printed: {filename}")
        else:
            print("Student not found")

    # --- Daily Roster ---
    def get_daily_roster(self, day):
        roster = []
        for c in self.courses:
            teacher = self.find_teacher(c.teacher_id)
            for lesson in c.lessons:
                if lesson['day'].lower() == day.lower():
                    roster.append({
                        "course_name": c.name,
                        "teacher_name": teacher.name,
                        "time": lesson['start_time'],
                        "room": lesson['room']
                    })
        return roster

    def print_daily_roster(self, day):
        lessons = self.get_daily_roster(day)
        if not lessons:
            print(f"No lessons on {day}")
            return

        widths = {
            "Time": max(len("Time"), *(len(l["time"]) for l in lessons)),
            "Course": max(len("Course"), *(len(l["course_name"]) for l in lessons)),
            "Teacher": max(len("Teacher"), *(len(l["teacher_name"]) for l in lessons)),
            "Room": max(len("Room"), *(len(l["room"]) for l in lessons))
        }
        padding = 3
        header = f"{'Time':<{widths['Time']+padding}}{'Course':<{widths['Course']+padding}}{'Teacher':<{widths['Teacher']+padding}}{'Room':<{widths['Room']}}"
        print(header)
        print("-"*len(header))
        for l in lessons:
            print(f"{l['time']:<{widths['Time']+padding}}{l['course_name']:<{widths['Course']+padding}}{l['teacher_name']:<{widths['Teacher']+padding}}{l['room']:<{widths['Room']}}")

    # --- Admin/Password ---
    def validate_admin(self, password):
        return password == self.ADMIN_PASSWORD

    def validate_student_access(self, password):
        return password in [self.STUDENT_PASSWORD, self.ADMIN_PASSWORD]
