from app.school_manager import SchoolManager

def student_menu(manager):
    print("\n--- Student Operations ---")
    print("1. Register Student")  # Already public
    print("2. Enroll in New Instrument")  # Requires student password
    print("3. Print Student Card")
    print("4. List Students")
    print("5. Search Student")
    print("r. Return")
    choice = input("Choice: ")

    if choice == "1":
        name = input("Student Name: ")
        instrument = input("Instrument: ")
        manager.add_student(name, instrument)

    elif choice == "2":
        pwd = input("Enter student password: ")
        if manager.validate_student_password(pwd):
            sid = input("Student ID: ")
            instrument = input("New Instrument: ")
            manager.enroll_student_in_course(sid, instrument)
        else:
            print("Invalid student password!")

    elif choice == "3":
        sid = input("Student ID: ")
        manager.print_student_card(sid)

    elif choice == "4":
        manager.list_students()

    elif choice == "5":
        term = input("Enter ID or Name: ")
        s = manager.find_student(term)
        if s:
            print(f"{s.id}: {s.name} Enrolled in {s.enrolled_in}")
        else:
            print("Student not found")
    
    elif choice.lower() == "r":
        return
    else:
        print("Invalid choice")


def course_menu(manager):
    print("\n--- Course & Enrollment ---")
    print("1. Add Course")  # Admin-only
    print("2. Daily Roster / Check-in")  # Public
    print("3. Switch Student Course (Admin Only)")
    print("r. Return")
    choice = input("Choice: ")

    if choice == "1":
        pwd = input("Admin password required: ")
        if manager.validate_admin(pwd):
            cname = input("Course Name: ")
            instr = input("Instrument: ")
            tid = input("Teacher ID: ")
            manager.add_course(cname, instr, tid)
        else:
            print("Wrong password!")

    elif choice == "2":
        print("1. Check-in Student\n2. Daily Roster")
        sub = input("Choice: ")
        if sub == "1":
            sid = input("Student ID: ")
            cid = input("Course ID: ")
            manager.check_in(sid, cid)
        elif sub == "2":
            day = input("Day: ")
            manager.print_daily_roster(day)
        else:
            print("Invalid choice")

    elif choice == "3":
        pwd = input("Admin password required: ")
        if manager.validate_admin(pwd):
            sid = input("Student ID: ")
            from_cid = input("From Course ID: ")
            to_cid = input("To Course ID: ")
            manager.switch_student_course(sid, from_cid, to_cid)
        else:
            print("Wrong password!")
    elif choice.lower() == 'r':
        return

    else:
        print("Invalid choice")

def admin_menu(manager):
    pwd = input("Enter admin password: ")
    if not manager.validate_admin(pwd):
        print("Wrong password!")
        return

    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Teacher")
        print("2. Update Teacher/Student")
        print("3. Remove Teacher/Student")
        print("4. Switch Student Course")
        print("5. Add Lesson to Course")
        print("r. Return")

        choice = input("Choice: ")

        if choice == "1":
            # Add Teacher
            name = input("Teacher Name: ")
            specialty = input("Specialty: ")
            manager.add_teacher(name, specialty)

        elif choice == "2":
            # Update Teacher/Student
            print("\nUpdate Options:")
            print("1. Update Student")
            print("2. Update Teacher")
            update_choice = input("Choice: ")

            if update_choice == "1":
                sid = input("Enter Student ID: ")
                student = manager.find_student(sid)
                if not student:
                    print("Student not found.")
                    continue
                print(f"Student: {student.name}, Enrolled: {student.enrolled_in}")
                print("1. Change Name")
                print("2. Update Enrollment")
                print("3. Cancel")
                s_choice = input("Choice: ")
                if s_choice == "1":
                    new_name = input("Enter new name: ")
                    student.name = new_name
                    manager._save_data()
                    print("Student name updated.")
                elif s_choice == "2":
                    new_enroll = input("Enter instruments separated by comma: ")
                    student.enrolled_in = [i.strip() for i in new_enroll.split(",")]
                    manager._save_data()
                    print("Student enrollment updated.")
                elif s_choice == "3":
                    continue
                else:
                    print("Invalid choice.")

            elif update_choice == "2":
                tid = input("Enter Teacher ID: ")
                teacher = manager.find_teacher(tid)
                if not teacher:
                    print("Teacher not found.")
                    continue
                print(f"Teacher: {teacher.name}, Specialty: {teacher.speciality}")
                print("1. Change Name")
                print("2. Change Specialty")
                print("3. Cancel")
                t_choice = input("Choice: ")
                if t_choice == "1":
                    new_name = input("Enter new name: ")
                    teacher.name = new_name
                    manager._save_data()
                    print("Teacher name updated.")
                elif t_choice == "2":
                    new_spec = input("Enter new specialty: ")
                    teacher.speciality = new_spec
                    manager._save_data()
                    print("Teacher specialty updated.")
                elif t_choice == "3":
                    continue
                else:
                    print("Invalid choice.")

        elif choice == "3":
            # Remove Teacher/Student
            print("\nRemove Options:")
            print("1. Remove Student")
            print("2. Remove Teacher")
            r_choice = input("Choice: ")

            if r_choice == "1":
                sid = input("Enter Student ID: ")
                student = manager.find_student(sid)
                if not student:
                    print("Student not found.")
                    continue
                confirm = input(f"Are you sure you want to remove {student.name}? (y/n): ")
                if confirm.lower() == "y":
                    manager.remove_student(sid)
            elif r_choice == "2":
                tid = input("Enter Teacher ID: ")
                teacher = manager.find_teacher(tid)
                if not teacher:
                    print("Teacher not found.")
                    continue
                confirm = input(f"Are you sure you want to remove {teacher.name}? (y/n): ")
                if confirm.lower() == "y":
                    manager.remove_teacher(tid)
            else:
                print("Invalid choice.")

        elif choice == "4":
            # Switch Student Course
            sid = input("Student ID: ")
            from_cid = input("From Course ID: ")
            to_cid = input("To Course ID: ")
            manager.switch_student_course(sid, from_cid, to_cid)

        elif choice == "5":
            # Add Lesson to Course
            cid = input("Course ID: ")
            day = input("Day (e.g., Monday): ")
            start = input("Start Time (HH:MM): ")
            room = input("Room: ")
            manager.add_lesson_to_course(cid, day, start, room)

        elif choice.lower() == "r":
            break

        else:
            print("Invalid choice.")

def teacher_menu(manager):
    print("\n--- Teacher Operations ---")
    print("1. List Teachers")
    print("2. Search Teacher")
    print("r. Return")
    choice = input("Choice: ")

    if choice == "1":
        manager.list_teachers()
    elif choice == "2":
        term = input("Enter ID or Name: ")
        t = manager.find_teacher(term)
        if t:
            print(f"{t.id}: {t.name} Specialty {t.specialty}")
        else:
            print("Teacher not found")
    elif choice.lower() == "r":
        return
    else:
        print("Invalid choice")

def main():
    manager = SchoolManager()
    while True:
        print("\n=== MSMS Menu ===")
        print("1. Student Operations")
        print("2. Teacher Operations")
        print("3. Courses & Enrollment")
        print("4. Attendance / Daily Roster")
        print("5. Admin Features")
        print("q. Quit")

        choice = input("Enter choice: ").lower()

        if choice == "1":
            student_menu(manager)
        elif choice == "2":
            teacher_menu(manager)
        elif choice == "3":
            course_menu(manager)
        elif choice == "4":
            # Check-in and daily roster together
            print("\n1. Check-in Student\n2. Daily Roster")
            sub = input("Choice: ")
            if sub == "1":
                sid = input("Student ID: ")
                cid = input("Course ID: ")
                manager.check_in(sid, cid)
            elif sub == "2":
                day = input("Day: ")
                manager.print_daily_roster(day)
            else:
                print("Invalid choice")
        elif choice == "5":
            admin_menu(manager)
        elif choice == "q":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()


