# Fragment 1

class Student:
    def __init__(self,name,ID,serial_number):
        self.serial_number = serial_number
        self.name = name
        self.ID = ID
        self.instrument = []

class Teacher:
    def __init__(self,name,ID,specialty,serial_number):
        self.serial_number = serial_number
        self.name = name
        self.ID = ID
        self.specialty = specialty

student_db = []
teacher_db = []
student_serial_counter = 1
teacher_serial_counter = 1

#Fragment 2

def is_ID_valid(ID):
    if len(str(ID)) != 8:
        return False
    if not str(ID).isdigit():
        return False
    if str(ID).startswith('0'):
        return False
    if find_student_by_id(int(ID)) or find_teacher_by_id(int(ID)):
        return False
    return True

def add_teacher(name,ID,specialty):
    global teacher_serial_counter

    if not is_ID_valid(ID):
        print("Error: The number entered is invalid! Please try again")
        return

    new_teacher = Teacher(name,ID,specialty,teacher_serial_counter)
    teacher_db.append(new_teacher)
    print(f"Core: Registered teacher '{name}' (ID: {ID}), specialty: '{specialty}'.")
    teacher_serial_counter +=1


def list_student():
    print("\n---- Student List ----")
    if len(student_db) == 0:
        print("No student is recorded in the system.")
        return

    max_name_len = max(len(student.name) for student in student_db)
    max_enrolled_len = max((len(', '.join(student.instrument)) for student in student_db),default=7)

    print(f"\n{'No.':<5}{'Name':<{max_name_len+2}}{'ID':<12}{'Enrolled':<{max_enrolled_len+2}}")
    print("-" * (5 + max_name_len + 2 + 12 + max_enrolled_len + 2))

    for student in student_db:
        enrolled = ', '.join(student.instrument)
        print(f"{student.serial_number:<5}{student.name:<{max_name_len+2}}{student.ID:<12}{enrolled:<{max_enrolled_len+2}}")

def list_teacher():
    print("\n---- Teacher List ----")
    if len(teacher_db) == 0:
        print("No teacher is recorded in the system.")
        return

    max_name_len = max(len(teacher.name) for teacher in teacher_db)
    max_specialty_len = max((len(teacher.specialty) for teacher in teacher_db))

    print(f"\n{'No.':<5}{'Name':<{max_name_len+2}}{'ID':<12}{'Enrolled':<{max_specialty_len+2}}")
    print("-" * (5 + max_name_len + 2 + 12 + max_specialty_len + 2))

    for teacher in teacher_db:
        print(f"{teacher.serial_number:<5}{teacher.name:<{max_name_len+2}}{teacher.ID:<12}{teacher.specialty:<{max_specialty_len+2}}")

def find_student(term):
    
    print(f"\n--- Finding Students matching '{term}' ---")
    result = []
    for student in student_db:
        if term.lower() in student.name.lower():
            result.append(student)
    if not result:
        print("No match found")
    else:
        for student in result:
            enrolled = ",".join(student.instrument)
            print(f"Serial: {student.serial_number}, Name: {student.name}, ID: {student.ID}, Enrolled: {enrolled}")

def find_teacher(term):

    print(f"\n--- Finding Teachers matching '{term} ---")
    result = []
    for teacher in teacher_db:
        if term.lower() in teacher.name.lower() or term.lower() in teacher.specialty.lower():
            result.append(teacher)
    if not result:
        print("No match found")
    else:
        for teacher in result:
            print(f"Serial: {teacher.serial_number}, Name: {teacher.name}, ID: {teacher.ID}, Specialty: {teacher.specialty}")

# Fragment 3

def find_student_by_id(student_id):
    for student in student_db:
        if student.ID == student_id:
            return student
    return None

def find_teacher_by_id(teacher_id):
    for teacher in teacher_db:
        if teacher.ID == teacher_id:
            return teacher
    return None

def front_desk_register(name,student_id,instrument):
    global student_serial_counter

    if not is_ID_valid(student_id):
        print("Error: ID entered is invalid!")
        print("Please make sure the ID entered is 8 digits and not duplicate!")
        return
    
    new_student = Student(name,student_id,student_serial_counter)
    student_db.append(new_student)
    student_serial_counter +=1

    front_desk_enrol(student_id,instrument)
    print(f"Front Desk: Registered {name} (ID: {student_id} enrolled in {instrument}")

def front_desk_enrol(student_id,instrument):
    student = find_student_by_id(student_id)
    if student:
        student.instrument.append(instrument)
    else:
        print(f"Error: Student ID {student_id} not found.")

def front_desk_lookup(term):
    find_student(term)
    find_teacher(term)
    if term.isdigit():
        student = find_student_by_id(int(term))
        if student:
            enrolled = ', '.join(student.instrument)
            print(f"ID Match: Serial: {student.serial_number}, Name: {student.name}, Enrolled: {enrolled}")
        
        teacher = find_teacher_by_id(int(term))
        if teacher:
            print(f"ID Match: Serial: {teacher.serial_number}, Name: {teacher.name}, Specialty: {teacher.specialty}")

# Fragment 4

def main():
    while True:
        print("\n===== Music School Front Desk =====")
        print("1. Register New Student")
        print("2. Enrol Existing Student")
        print("3. Lookup Student or Teacher")
        print("4. (Admin) List all Students")
        print("5. (Admin) List all Teachers")
        print("6. (Admin) Adding new Teacher")
        print("q. Quit")

        choice = input("Please enter your choice: ")
        if choice == "1":
            name = input("Enter your student name: ")
            student_id = input("Enter your student id: ")
            instrument = input("Enter the instrument you enrol in: ")
            front_desk_register(name,student_id,instrument)
        
        elif choice == "2":
            student_id = input("Enter your student ID: ")
            instrument = input("Enter instrument to enrol in: ")
            try:
                student_id = int(student_id)
                front_desk_enrol(student_id,instrument)
            except ValueError:
                print("Please enter a valid student id")
        
        elif choice == "3":
            term = input("Enter search term: ")
            front_desk_lookup(term)
        
        elif choice == "4":
            list_student()
        
        elif choice == "5":
            list_teacher()
        
        elif choice == "6":
            name = input("Enter your name: ")
            teacher_id = input("Enter your teacher id: ")
            specialty = input("Enter your teaching specialty: ")
            add_teacher(name,teacher_id,specialty)

        elif choice.lower() == "q":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Error: Invalid Choice.Please try again")

if __name__ == "__main__":
    main()