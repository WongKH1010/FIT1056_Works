import json, os, datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path=os.path.dirname(__file__)):
        self.data_path = os.path.join(data_path, '..', 'data', 'msms.json')
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.next_lesson_id = 1
        self.next_student_id = 1
        self.next_teacher_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                self.teachers = [TeacherUser(**t) for t in data.get("teachers", [])]
                self.students = [StudentUser(**s) for s in data.get("students", [])]
                self.courses = [Course(**c) for c in data.get("courses", [])]
                self.attendance_log = data.get("attendance",[])
                self.next_student_id = max([s["id"] for s in data.get("students", [])], default=0) + 1
                self.next_teacher_id = max([t["id"] for t in data.get("teachers", [])], default=0) + 1
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""

        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            "attendance" : self.attendance_log
        }
        with open(self.data_path, "w") as f:
            json.dump(data_to_save, f, indent=4)
    
    def find_student(self, term):
        for s in self.students:
            if str(s.id) == str(term) or term.lower() in s.name.lower():
                return s
        return None
    
    def list_student(self,id,name):
        found = []
        for s_2 in self.students:
            if str(s_2.id) == str(id).strip() or str(name).lower().strip() in str(s_2.name).lower().strip():
                found.append({
                    "ID": s_2.id,
                    "Name": s_2.name,
                    "Enrolled Courses": s_2.enrolled_course_ids
                })
        return found
    
    def find_student_pro(self,id,name):
        found_s_2 = []
        for s_2 in self.students:
            if str(s_2.id) == str(id).strip() and str(name).lower().strip() in str(s_2.name).lower().strip():
                found_s_2.append({
                    "ID": s_2.id,
                    "Name": s_2.name,
                    "Enrolled Course": s_2.enrolled_course_ids
                })
        return found_s_2
    
    def find_teacher(self, term):
        for t in self.teachers:
            if str(t.id) == str(term) or term.lower() in t.name.lower():
                return t
        return None

    def list_teacher(self,id,name):
        found = []
        for t_2 in self.teachers:
            if str(t_2.id) == str(id).strip() or str(name).lower().strip() in str(t_2.name).lower().strip():
                found.append({
                    "ID": t_2.id,
                    "Name": t_2.name,
                    "Speciality": t_2.speciality
                })
        return found
        
    def find_teacher_pro(self,id,name):
        found_t_2 = []
        for t_2 in self.teachers:
            if str(t_2.id) == str(id).strip() and str(name).lower().strip() in str(t_2.name).lower().strip():
                found_t_2.append({
                    "ID": t_2.id,
                    "Name": t_2.name,
                    "Speciality": t_2.speciality
                })
        return found_t_2
    
    def find_course(self, term):
        for c in self.courses:
            if str(c.id) == str(term):
                return c

    
    def register_new_student(self,name,instrument):
        for c_id in self.courses:
            if c_id.instrument.lower() == instrument.lower():
                student = StudentUser(self.next_student_id, name, [c_id.id])
                self.students.append(student)
                c_id.enroll_student(self.next_student_id)
                self.next_student_id += 1
                self._save_data()
                return student
        return False

    def add_teacher(self, name, specialty):
        teacher = TeacherUser(self.next_teacher_id, name, specialty)
        self.teachers.append(teacher)
        self.next_teacher_id += 1
        self._save_data()
        return teacher

    def check_in(self, student_id, course_id):
            self.attendance_log.append({
                "student_id": student_id,
                "course_id": course_id,
                "timestamp": datetime.datetime.now().isoformat()
            })
            self._save_data()
            return True

    
    def add_course(self, name, instrument, teacher_id):
        teacher = self.find_teacher(teacher_id)
        if not teacher:
            return False
        course_id = max([c.id for c in self.courses], default=100) + 1
        course = Course(course_id, name, instrument, teacher_id)
        course.enrolled_student_ids = []
        course.lessons = []
        self.courses.append(course)
        self._save_data()
        return course

    def add_lesson_to_course(self, course_id, day, start_time, room):
        """Admin-only: Adds a lesson to a course."""
        course = self.find_course(course_id)
        if not course:
            return False

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
        return lesson

    def switch_course(self, student_id, from_course_id, to_course_id):
        student = self.find_student(student_id)
        from_course = self.find_course(from_course_id)
        to_course = self.find_course(to_course_id)

        if not all([student, from_course, to_course]):
            return False

        if from_course_id not in student.enrolled_course_ids:
            return False

        if to_course_id in student.enrolled_course_ids:
            return False

        student.enrolled_course_ids.remove(from_course_id)
        student.enrolled_course_ids.append(to_course_id)
        from_course.remove_student(student_id)
        to_course.enroll_student(student_id)
        return True

    def enroll_student_in_course(self, student_id, course_id):
        student = self.find_student(student_id)
        course = self.find_course(course_id)
        if student and course:
            student.enroll_in(course.id)
            course.enroll_student(student.id)
            self._save_data()

    def update_teacher(self, teacher_id, new_name=None, new_speciality=None):
        teacher = self.find_teacher(teacher_id)
        if not teacher:
            return False
        
        if new_name:
            teacher.name = new_name
        if new_speciality:
            teacher.speciality = new_speciality

        self._save_data()
        return True
    
