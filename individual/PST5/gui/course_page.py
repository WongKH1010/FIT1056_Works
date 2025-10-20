import streamlit as st
import pandas as pd

def show_course_page(manager):
    st.header("Course Management")

    st.subheader("Add Course")
    teacher_list = [
        {"ID": t.id, "Name": t.name, "Speciality": t.speciality}
        for t in manager.teachers
    ]

    if not manager.teachers:
        st.error("Please add a teacher first")
    else:
        with st.form("add_course"):
            df = pd.DataFrame(teacher_list)
            name = st.text_input("Enter the course name")
            st.dataframe(df, hide_index=True)
            
            selected_teacher = st.selectbox(
                "Select a teacher:",
                options=df["Name"],
                index=None,
                placeholder="Choose one..."
            )

            submitted = st.form_submit_button("Add Course")

            if submitted:
                if selected_teacher:
                    teacher = df[df["Name"] == selected_teacher].iloc[0]
                    teacher_id = teacher["ID"]
                    instrument = teacher["Speciality"]
                    success = manager.add_course(name, instrument, teacher_id)
                    if success:
                        st.success(
                            f"Course '{name}' added with {instrument}, taught by Teacher ID {teacher_id}"
                        )
                else:
                    st.warning("Please select a teacher first.")

    st.subheader("Add lesson to course")
    with st.form("select_course"):
        course_list = [
            {"ID": c.id, "Name": c.name, "Instrument": c.instrument, "Lessons": c.lessons}
            for c in manager.courses
        ]

        df = pd.DataFrame(
            [{"ID": c["ID"], "Name": c["Name"], "Instrument": c["Instrument"]}
             for c in course_list]
        )
        st.dataframe(df, hide_index=True)

        selected_course = st.selectbox(
            "Select a course:",
            options=df["Name"],
            index=None,
            placeholder="Choose one..."
        )

        submitted = st.form_submit_button("Select Course")

    if submitted:
        if selected_course:
            course = next(c for c in course_list if c["Name"] == selected_course)
            st.subheader(f"Existing Lessons for {course['Name']} ({course['Instrument']})")

            lessons = course["Lessons"]

            if lessons:
                lessons_df = pd.DataFrame(lessons)
                st.table(lessons_df)
            else:
                st.info("No lessons exist for this course yet.")
            
            with st.form("Add lessons"):
                st.write("Enter the information of the lesson you want to add")
                day = st.text_input("Day of lesson")
                start_time = st.text_input("Start time")
                room = st.text_input("Room")
                submit = st.form_submit_button("Submit")
                if submit:
                    add_lessons = manager.add_lesson_to_course(course['ID'], day, start_time, room)
                    if add_lessons:
                        st.success(f"Lesson ID: {add_lessons['lesson']} on {day} at {start_time} in {room} is added")
                    else:
                        st.warning("Please enter valid information")
        else:
            st.warning("Please select a course first.")
