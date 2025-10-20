import streamlit as st
from app.admin_utils import backup_data

def show_home_page(manager):
    st.title("🎶 Music School Management System")
    st.markdown("---")

    st.subheader("👋 Welcome")
    st.write(
        """
        This system helps manage teachers, courses, students, and lessons 
        in a simple and efficient way.  
        
        Use the sidebar to navigate through different sections of the system.
        """
    )

    st.subheader("📌 Features Overview")
    st.write(
        """
        - **Teacher Management**: Add, update, and view teacher information.  
        - **Course Management**: Create and assign courses to teachers.  
        - **Lesson Scheduling**: Organize and manage lessons for each course.  
        - **Student Management**: Enroll students and track their progress.  
        - **Switch & Enrollment**: Manage course enrollment and switching for students.  
        """
    )

    st.subheader("✨ How to Use")
    st.write(
        """
        1. Start by adding **teachers** to the system.  
        2. Create **courses** and assign them to teachers.  
        3. Add **lessons** to courses (e.g., time, day, room).  
        4. Enroll **students** into courses.  
        5. Use the system to track and update as the school grows.  
        """
    )

    st.markdown("---")
    st.info("Use the sidebar on the left to explore the system.")

    st.subheader("Backup Now")
    back_up = st.button("Back up")
    if back_up:
        backup_data()