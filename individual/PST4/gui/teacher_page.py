import streamlit as st
import pandas as pd


def show_teacher_update_page(manager):
    st.header("Teacher Management")
    st.subheader("Find a Teacher")

    with st.form("find_teacher"):
        find_name = st.text_input("Enter the teacher name you want to find")
        find_id = st.text_input("Enter the teacher id you want to find")
        st.caption("You can enter both or either one")
        find = st.form_submit_button("Search")

        if find:
            if (find_name and not find_id) or (find_id and not find_name):
                found = []
                for f in manager.find_teacher(find_name or find_id):
                    if f:
                        found.append({
                            "id": f.id,
                            "name": f.name,
                            "speciality": f.speciality
                        })
                    else:
                        st.warning("No teacher found")
                df = pd.DataFrame(found)  # found is already a list of dicts
                st.dataframe(df)
            elif find_name and find_id:
                found = manager.find_teacher_pro(find_id, find_name)
                if found:
                    df = pd.DataFrame(found)  # found is already a list of dicts
                    st.dataframe(df)
                else:
                    st.warning("No teacher found")
            else:
                st.error("Please enter a name, an ID, or both to search.")

    # ...

    # --- Registration Section (now works correctly) ---
    st.subheader("Register New teacher")
    with st.form("registration_form"):
        reg_name = st.text_input("New teacher Name")
        reg_instrument = st.text_input("First Instrument")
        submitted = st.form_submit_button("Register teacher")
        
        if submitted:
            # This call now works because we implemented the method in PST3.
            # TODO: Add a check for blank name/instrument.
            if reg_name and reg_instrument:
                new_teacher = manager.add_teacher(reg_name, reg_instrument)
                if new_teacher:
                    st.success(f"Successfully added {reg_name}!")
                    # You can use st.balloons() for extra flair.
                else:
                    st.error(f"Could not register teacher. A teacher for {reg_instrument} might not be available.")
            else:
                st.warning("Please enter both a name and a speciality.")

                
    st.subheader("Update Teacher Information")
    teacher_list = [
        {"ID": t.id, "Name": t.name, "Speciality": t.speciality}
        for t in manager.teachers
    ]

    if not manager.teachers:
        st.warning("No teachers found. Please add a teacher first.")
        return

    st.write("### Current Teachers")
    st.table(pd.DataFrame(teacher_list))

    with st.form("update_teacher_form"):
        teacher_id = st.selectbox(
            "Select Teacher to Update",
            [t["ID"] for t in teacher_list],
            format_func=lambda x: next(t["Name"] for t in teacher_list if t["ID"] == x)
        )

        new_name = st.text_input("New Name (leave blank to keep current)")
        new_speciality = st.text_input("New Speciality (leave blank to keep current)")

        submitted = st.form_submit_button("Update Teacher")

        if submitted:
            success = manager.update_teacher(
                teacher_id,
                new_name if new_name.strip() else None,
                new_speciality if new_speciality.strip() else None
            )
            if success:
                st.success(f"Teacher {teacher_id} updated successfully.")
            else:
                st.error("Failed to update teacher. Please try again.")