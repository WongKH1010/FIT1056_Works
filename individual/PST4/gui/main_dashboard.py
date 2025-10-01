# gui/main_dashboard.py
import streamlit as st
from app.schedule import ScheduleManager
from gui.student_pages import show_student_management_page
from gui.roster_pages import show_roster_page
from gui.home_page import show_home_page
from gui.course_page import show_course_page


def launch():

    st.set_page_config(layout="wide", page_title="Music School Management System")
    if 'manager' not in st.session_state:
        st.session_state.manager = ScheduleManager()

    st.sidebar.title("MSMS Navigation")

    page = st.sidebar.radio("Go to", ["Home Page","Student Management", "Daily Roster", "Payments (stub)"])


    if page == "Home Page":
        show_home_page(st.session_state.manager)
    elif page == "Student Management":
        show_student_management_page(st.session_state.manager)
    elif page == "Daily Roster":
        show_roster_page(st.session_state.manager)
    elif page == "Course Page":
        show_course_page()
    elif page == "Payments (stub)":
        st.header("Payments")
        st.warning("This feature will be implemented in PST5.")