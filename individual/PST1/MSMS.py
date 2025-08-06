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
    new_teacher = Teacher(name,teacher_ID_counters,specialty)
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
        if find.lower() in term.name.lower():
            result.append(term)
    if len(result) == 0:
        print("\nNo match found")
    else:
        for student in result:
            enrolled = ",".join(student.instrument_learning)
            print(f"Name: {student.name}, ID: {student.ID}, Enrolled: {enrolled}")            
    pass

def find_teachers(find):
    print(f"\n--- Finding Teachers matching '{find}' ---")
    result = []
    for term in teacher_db:
        if find.lower() in term.name.lower() or str(term.specialty) == find:
            result.append(term)
    if len(result) == 0:
        print("\nNo match found")
    else:
        for teacher in result:
            print(f"Name: {teacher.name}, ID: {teacher.ID}, Specialty: {teacher.specialty}")
    pass

def find_student_by_id(student_id):
    for student in student_db:
        if student.ID == student_id:
            return student
    return None

def front_desk_register(name, instrument):
    global student_ID_counters
    new_student = Student(name, student_ID_counters)
    student_db.append(new_student)
    student_ID_counters += 1
    
    front_desk_enrol(new_student.ID, instrument)
    print(f"Front Desk: Successfully registered '{name}' and enrolled them in '{instrument}'.")

def front_desk_enrol(student_id, instrument):
    student = find_student_by_id(student_id)
    if student:
        student.instrument_learning.append(instrument)
        print(f"Front Desk: Enrolled student {student_id} in '{instrument}'.")
    else:
        print(f"Error: Student ID {student_id} not found.")

def front_desk_lookup(term):
    print(f"\n--- Performing lookup for '{term}' ---")
    find_students(term)
    find_teachers(term)

def main():
    while True:
        print("\n===== Music School Front Desk =====")
        print("1. Register New Student")
        print("2. Enrol Existing Student")
        print("3. Lookup Student or Teacher")
        print("4. (Admin) List all Students")
        print("5. (Admin) List all Teachers")
        print("q. Quit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter student name: ")
            instrument = input("Enter instrument to enrol in: ")
            front_desk_register(name, instrument)
        elif choice == '2':
            try:
                student_id = int(input("Enter student ID: "))
                instrument = input("Enter instrument to enrol in: ")
                front_desk_enrol(student_id, instrument)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '3':
            term = input("Enter search term: ")
            front_desk_lookup(term)
        elif choice == '4':
            list_students()
        elif choice == '5':
            list_teachers()
        elif choice.lower() == 'q':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()