import json, os, datetime, csv, logging
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path=None):
        if data_path is None:
            # default to your production JSON file
            self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'msms.json')
        else:
            # use test file or custom path from fixture
            self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.next_lesson_id = 1
        self.next_student_id = 1
        self.next_teacher_id = 1
        self.finance_log = []
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                self.teachers = [TeacherUser(**t) for t in data.get("teachers", [])]
                self.students = [StudentUser(**s) for s in data.get("students", [])]
                self.courses = [Course(**c) for c in data.get("courses", [])]
                self.finance_log = data.get("finance",[])
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
            "attendance" : self.attendance_log,
            "finance" : self.finance_log
        }
        with open(self.data_path, "w") as f:
            json.dump(data_to_save, f, indent=4)
    
    def find_student(self, term):
        for s in self.students:
            if str(s.id) == str(term) or str(term).lower() in s.name.lower():
                return s
        return None
    
    def list_student(self,term):
        found = []
        for s_2 in self.students:
            if str(s_2.id) == str(term).strip() or str(term).lower().strip() in str(s_2.name).lower().strip():
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
            if str(t.id) == str(term) or str(term).lower() in t.name.lower():
                return t
        return None

    def list_teacher(self,term):
        found = []
        for t_2 in self.teachers:
            if str(t_2.id) == str(term).strip() or str(term).lower().strip() in str(t_2.name).lower().strip():
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
                logging.info(f"Successfully registered student: '{name} ID: {self.next_student_id} Enrolled in : {instrument}'")
                self.next_student_id += 1
                self._save_data()
                return student
        return False

    def add_teacher(self, name, specialty):
        teacher = TeacherUser(self.next_teacher_id, name, specialty)
        self.teachers.append(teacher)
        logging.info(f"Successfully added teacher: '{name} ID: {self.next_teacher_id} Specialty : {specialty}'")
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
            logging.info(f"Successfully check in 'Student ID: {self.next_student_id}  Course ID : {course_id}'")
            return True

    
    def add_course(self, name, instrument, teacher_id,fee):
        teacher = self.find_teacher(teacher_id)
        if not teacher:
            return False
        course_id = max([c.id for c in self.courses], default=100) + 1
        course = Course(course_id, name, instrument, teacher_id,[], [],fee)
        self.courses.append(course)
        self._save_data()
        logging.info(f"Successfully added course 'Course ID: {course_id}  Course Name : {name}'")
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
        logging.info(f"Successfully added lesson 'Lesson ID : {lesson_id} to  Course ID : {course_id}'")
        return lesson
    
    def cancel_lesson(self, course_id,lesson_id, reason):
        # ... (logic to cancel a lesson) ...
        c = self.find_course(course_id)
        if c:
            pass
        else:
            return False
        for l in c.lessons:
            for l_id in l:
                if l_id == lesson_id:
                    c.lessons.remove(l)
                else:
                    return False
        self._save_data()
        # TODO: Add a log entry.
        logging.warning(f"Lesson ID {lesson_id} was cancelled. Reason: {reason}")

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
        logging.info(f"Successfully switched course 'Student ID: {student} from {from_course_id} to {to_course_id}'")
        return True

    def enroll_student_in_course(self, student_id, course_id):
        student = self.find_student(student_id)
        course = self.find_course(course_id)
        if student and course:
            student.enroll_in(course.id)
            course.enroll_student(student.id)
            self._save_data()
            logging.info(f"Successfully enrolled: 'Student : {student.name} ID: {student_id} Enrolled in: {course.name}'")

    def update_teacher(self, teacher_id, new_name=None, new_speciality=None):
        teacher = self.find_teacher(teacher_id)
        if not teacher:
            return False
        
        if new_name:
            teacher.name = new_name
        if new_speciality:
            teacher.speciality = new_speciality

        self._save_data()
        logging.info(f"Successfully updated teacher info '{new_name} ID: {teacher_id} Specialty: {new_speciality}'")
        return True
    
    def record_payment(self, student_id, amount, method):
        """Adds a payment record to the finance log."""
        # TODO: Find the student to ensure they exist.
        s = self.find_student(student_id)
        if s:
            pass
        else:
            return False
        # Create a payment dictionary with student_id, amount, method, and a timestamp.
        payment_record = {
            "student_id": student_id,
            "amount": amount,
            "method": method,
            "timestamp": datetime.datetime.now().isoformat()
        }
        # TODO: Append the record to self.finance_log and save the data.
        self.finance_log.append(payment_record)
        self._save_data()
        print(f"Payment of {amount} for student {student_id} recorded.")
        logging.info(f"Payment recorded: 'Student {s.name} ID {s.id} Amount : ${amount} Payment Method: {method}'")

    def get_payment_history(self, student_id):
        """Returns a list of all payments for a given student."""
        # TODO: Use a list comprehension to filter self.finance_log
        # and return only the records that match the student_id.
        return [p for p in self.finance_log if p['student_id'] == student_id]
    
    def get_student_bill(self, student_id):
        """Returns a summary of the student's billing, including total fees, payments, and balance."""
        student = self.find_student(student_id)
        if not student:
            print("Student not found.")
            return None

        # Calculate total course fees
        total_fees = 0.0
        enrolled_courses = []
        for cid in getattr(student, "enrolled_course_ids", []):
            course = self.find_course(cid)
            if course:
                total_fees += getattr(course, "fees", 0.0)
                enrolled_courses.append(course.id)

        # Calculate total paid
        payments = [p for p in self.finance_log if p["student_id"] == student_id]
        total_paid = sum(p["amount"] for p in payments)

        # Balance
        balance = total_fees - total_paid

        # Return full summary
        bill_summary = [{
            "student_id": student.id,
            "student_name": student.name,
            "courses": enrolled_courses,
            "total_fees": total_fees,
            "total_paid": total_paid,
            "balance_due": balance,
            "payment_history": payments
        }]

        return bill_summary


    def export_report(self, kind, out_path):
        """Exports a log to a CSV file."""
        print(f"Exporting {kind} report to {out_path}...")
        # TODO: Use an if/elif block to select the correct data list based on 'kind'.
        if kind == "finance":
            data_to_export = self.finance_log
            headers = ["student_id", "amount", "method", "timestamp"]
        elif kind == "attendance":
            data_to_export = self.attendance_log # Assuming this exists from PST2
            headers = ["student_id", "course_id", "timestamp"]
        else:
            print("Error: Unknown report type.")
            return
        
        try:
            with open(out_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data_to_export)
            return True
        except Exception as e:
            print(f"Error exporting error : {e} ")
            return False