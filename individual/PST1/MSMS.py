class Student:
    def __init__(self,name,student_ID):
        self.ID = student_ID
        self.name = name
        self.instrument_learning = []
    
class Teacher:
    def __init__(self,name,teacher_ID,specialty):
        self.ID = teacher_ID
        self.name = name
        self.specialty = specialty

student_db = []
teacher_db = []
student_ID_counters = 1
teacher_ID_counters = 1

def add_teacher(name,specialty):
    global teacher_ID_counters
    new_teacher = Teacher(teacher_ID_counters,name,specialty)
    teacher_db.append(new_teacher)
    teacher_ID_counters += 1
    print(f"Core: Teacher {name} is successfully added")

def list_students():
    print("\n----Student List----")
    if len(student_db) == 0:
        print("\nNo student is recorded in the system")
        return
    
    max_name_len = max(len(student.name) for student in student_db)
    max_enrolled_len = max((len(', '.join(student.instrument_learning)) for student in student_db))

    print(f"\n\n{'No.':<5}{'Name':<{max_name_len+2}}{'ID':<6}{'Enrolled':<{max_enrolled_len+2}}")
    print("-" * (5 + max_name_len + 2 + 6 + max_enrolled_len + 2))

    for i, student in enumerate(student_db, start=1):
        enrolled = ', '.join(student.instrument_learning)
        print(f"{i:<5}{student.name:<{max_name_len+2}}{student.ID:<6}{enrolled:<{max_enrolled_len+2}}")

def list_teachers():
    print("\n----Teacher List----")
    if len(teacher_db) == 0:
        print("\nNo teacher is recorded in the system")
        return
    
    max_name_len = max(len(teacher.name) for teacher in teacher_db)
    max_specialty_len = max(len(teacher.specialty) for teacher in teacher_db)

    print(f"\n\n{'No.':<5}{'Name':<{max_name_len+2}}{'ID':<6}{'Enrolled':<{max_specialty_len+2}}")
    print("-" * (5 + max_name_len + 2 + 6 + max_specialty_len + 2))

    for i, teacher in enumerate(teacher_db, start=1):
        print(f"{i:<5}{teacher.name:<{max_name_len+2}}{teacher.ID:<6}{teacher.specialty:<{max_specialty_len+2}}")

def find_students(find):
    print(f"\n--- Finding Students matching '{find}' ---")
    result = []
    for term in student_db:
        if find == term:
            result.append(find)
    if len(result) == 0:
        print("\nNo match found")
    else:
        print(result)
    





