# gui/student_pages.py
import pandas as pd
import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    st.subheader("Find a Student")

    with st.form("find_student"):
        find_name = st.text_input("Enter the student name you want to find")
        find_id = st.text_input("Enter the student id you want to find")
        st.caption("You can enter both or either one")
        find = st.form_submit_button("Search")

        if find:
            if (find_name and not find_id) or (find_id and not find_name):
                found = []
                for f in manager.find_student(find_name or find_id):
                    if f:
                        found.append({
                            "id": f.id,
                            "name": f.name,
                            "enrolled_course_ids": f.enrolled_course_ids
                        })
                    else:
                        st.warning("No student found")
                df = pd.DataFrame(found) 
                st.dataframe(df)
            elif find_name and find_id:
                found = manager.find_student_pro(find_id, find_name)
                if found:
                    df = pd.DataFrame(found)
                    st.dataframe(df)
                else:
                    st.warning("No student found")
            else:
                st.error("Please enter a name, an ID, or both to search.")
    
    st.divider()


    st.subheader("Register New Student")
    with st.form("registration_form"):
        reg_name = st.text_input("New Student Name")
        reg_instrument = st.text_input("First Instrument")
        submitted = st.form_submit_button("Register Student")
        
        if submitted:
            if reg_name and reg_instrument:
                new_student = manager.register_new_student(reg_name, reg_instrument)
                if new_student:
                    st.success(f"Successfully registered {reg_name}!")
                else:
                    st.error(f"Could not register student. A teacher for {reg_instrument} might not be available.")
            else:
                st.warning("Please enter both a name and an instrument.")
    
    st.divider()    
    st.subheader("Enroll Student in Course")

    student_list = [
        {"ID": s.id, "Name": s.name, "Enrolled": s.enrolled_course_ids}
        for s in manager.students
    ]
    course_list = [
        {"ID": c.id, "Name": c.name, "Instrument": c.instrument}
        for c in manager.courses
    ]
    st.write("Students")
    st.table(pd.DataFrame(student_list))

    st.write("Courses")
    st.table(pd.DataFrame(course_list))

    with st.form("enroll_student_form"):
        student_id = st.selectbox(
            "Select Student", [s["ID"] for s in student_list], format_func=lambda x: next(s["Name"] for s in student_list if s["ID"] == x)
        )
        course_id = st.selectbox(
            "Select Course", [c["ID"] for c in course_list], format_func=lambda x: next(c["Name"] for c in course_list if c["ID"] == x)
        )

        enroll_submit = st.form_submit_button("Enroll")

        if enroll_submit:
            success = manager.enroll_student_in_course(student_id, course_id)
            if success:
                st.success(f"Student {student_id} enrolled in course {course_id}.")
            else:
                st.error("Failed to enroll student. Check if already enrolled.")

    st.divider()

    st.subheader("Switch Course")

    with st.form("switch_course_form"):
        student_id = st.selectbox(
            "Select Student", [s["ID"] for s in student_list], format_func=lambda x: next(s["Name"] for s in student_list if s["ID"] == x), key="switch_student"
        )


        enrolled_courses = []
        student = manager.find_student(student_id)
        if student:
            enrolled_courses = [
                c for c in manager.courses if c.id in student.enrolled_course_ids
            ]

        from_course_id = st.selectbox(
            "From Course", [c.id for c in enrolled_courses], format_func=lambda x: next(c.name for c in enrolled_courses if c.id == x)
        )

        to_course_id = st.selectbox(
            "To Course", [c["ID"] for c in course_list], format_func=lambda x: next(c["Name"] for c in course_list if c["ID"] == x), key="to_course"
        )

        switch_submit = st.form_submit_button("Switch Course")

        if switch_submit:
            success = manager.switch_course(student_id, from_course_id, to_course_id)
            if success:
                st.success(f"Student {student_id} switched from course {from_course_id} to {to_course_id}.")
            else:
                st.error("Failed to switch course. Check if enrolled correctly or already in target course.")

