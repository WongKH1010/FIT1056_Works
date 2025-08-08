# === Models ===
class Student:
    def __init__(self, name, student_ID, serial_number):
        self.ID = student_ID
        self.name = name
        self.serial_number = serial_number
        self.instrument_learning = []

class Teacher:
    def __init__(self, name, teacher_ID, specialty, serial_number):
        self.ID = teacher_ID
        self.name = name
        self.specialty = specialty
        self.serial_number = serial_number

# === Databases and Counters ===
student_db = []
teacher_db = []

student_serial_counter = 1
teacher_serial_counter = 1


# === Validation ===
def is_valid_student_id(student_id):
    if not str(student_id).isdigit():
        return False
    if len(str(student_id)) != 8:
        return False
    if str(student_id).startswith('0'):
        return False
    if find_student_by_id(int(student_id)):
        return False
    return True

def is_valid_teacher_id(teacher_id):
    if not str(teacher_id).isdigit():
        return False
    if find_teacher_by_id(int(teacher_id)):
        return False
    return True

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


# === Core Functions ===
def front_desk_register(name, student_ID, instrument):
    global student_serial_counter

    if not is_valid_student_id(student_ID):
        print("Error: Invalid or duplicate student ID. Must be 8 digits, not start with 0, and unique.")
        return

    new_student = Student(name, int(student_ID), student_serial_counter)
    student_db.append(new_student)
    student_serial_counter += 1

    front_desk_enrol(new_student.ID, instrument)
    print(f"Front Desk: Registered '{name}' (ID: {student_ID}), enrolled in '{instrument}'.")

def front_desk_enrol(student_id, instrument):
    student = find_student_by_id(student_id)
    if student:
        student.instrument_learning.append(instrument)
        print(f"Front Desk: Enrolled student {student_id} in '{instrument}'.")
    else:
        print(f"Error: Student ID {student_id} not found.")

def add_teacher(name, teacher_ID, specialty):
    global teacher_serial_counter

    if not is_valid_teacher_id(teacher_ID):
        print("Error: Invalid or duplicate teacher ID. Must be numeric and unique.")
        return

    new_teacher = Teacher(name, int(teacher_ID), specialty, teacher_serial_counter)
    teacher_db.append(new_teacher)
    teacher_serial_counter += 1

    print(f"Core: Registered teacher '{name}' (ID: {teacher_ID}), specialty: '{specialty}'.")


# === Lookup Functions ===
def front_desk_lookup(term):
    print(f"\n--- Performing lookup for '{term}' ---")
    find_students(term)
    find_teachers(term)

def find_students(find):
    print(f"\n--- Finding Students matching '{find}' ---")
    result = [student for student in student_db if find.lower() in student.name.lower()]
    if not result:
        print("No match found.")
    else:
        for student in result:
            enrolled = ", ".join(student.instrument_learning)
            print(f"Serial: {student.serial_number}, Name: {student.name}, ID: {student.ID}, Enrolled: {enrolled}")

def find_teachers(find):
    print(f"\n--- Finding Teachers matching '{find}' ---")
    result = [teacher for teacher in teacher_db if find.lower() in teacher.name.lower() or find.lower() in teacher.specialty.lower()]
    if not result:
        print("No match found.")
    else:
        for teacher in result:
            print(f"Serial: {teacher.serial_number}, Name: {teacher.name}, ID: {teacher.ID}, Specialty: {teacher.specialty}")


# === List Functions ===
def list_students():
    print("\n---- Student List ----")
    if len(student_db) == 0:
        print("No student is recorded in the system.")
        return

    max_name_len = max(len(student.name) for student in student_db)
    max_enrolled_len = max((len(', '.join(student.instrument_learning)) for student in student_db), default=7)

    print(f"\n{'No.':<5}{'Name':<{max_name_len+2}}{'ID':<12}{'Enrolled':<{max_enrolled_len+2}}")
    print("-" * (5 + max_name_len + 2 + 12 + max_enrolled_len + 2))

    for student in student_db:
        enrolled = ', '.join(student.instrument_learning)
        print(f"{student.serial_number:<5}{student.name:<{max_name_len+2}}{student.ID:<12}{enrolled:<{max_enrolled_len+2}}")

def list_teachers():
    print("\n---- Teacher List ----")
    if len(teacher_db) == 0:
        print("No teacher is recorded in the system.")
        return

    max_name_len = max(len(teacher.name) for teacher in teacher_db)
    max_specialty_len = max(len(teacher.specialty) for teacher in teacher_db)

    print(f"\n{'No.':<5}{'Name':<{max_name_len+2}}{'ID':<10}{'Specialty':<{max_specialty_len+2}}")
    print("-" * (5 + max_name_len + 2 + 10 + max_specialty_len + 2))

    for teacher in teacher_db:
        print(f"{teacher.serial_number:<5}{teacher.name:<{max_name_len+2}}{teacher.ID:<10}{teacher.specialty:<{max_specialty_len+2}}")


# === Main Menu ===
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
            student_id = input("Enter 8-digit student ID (must not start with 0): ")
            instrument = input("Enter instrument to enrol in: ")
            front_desk_register(name, student_id, instrument)

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


# === Run Program ===
if __name__ == "__main__":
    main()
