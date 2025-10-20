# 🎵 Music School Management System v5 (OOP + Streamlit)

This is a **Python + Streamlit web application** for managing the front desk and administrative operations of a music school.  

It builds upon the previous **OOP architecture with persistent JSON storage**, but adds a **Streamlit GUI** for easier management.  

---

## ✨ Features

- 📝 **Register new students** with course enrollment  
- 🎶 **Enroll or switch students between courses**  
- 👩‍🏫 **Add and update teachers** with their specialty  
- 📚 **Add courses linked to teachers**  
- 📅 **Add lessons to courses** (day, time, room)  
- 📋 **View daily roster** of classes by weekday  
- 🛠 **Update student and teacher information**  
- 🔍 **Search teachers and students by ID or name**  
- 🕒 **Student attendance check-in**  
- 💾 **Persistent JSON data storage** 
- 💰 **Finance & Payments module** 

---

## 📁 Core Components

### 🔹 Data Management
- **Persistent JSON storage** for `students`, `teachers`, `courses`, and `attendance`.  
- Automatic saving with every action (`_save_data()`).  
- Auto-generated unique IDs for students and teachers.  

### 🔹 Classes
- **`Student`** — stores student info and enrolled courses.  
- **`Teacher`** — stores teacher info and specialty.  
- **`Course`** — stores lessons and enrolled students.  
- **`ScheduleManager` / `Manager`** — central logic for data handling.  

### 🔹 GUI Pages
- **🏠 Home Page** — Introduction & navigation overview.  
- **👩‍🎓 Student Page** — Register, search, enroll, and switch courses.  
- **👩‍🏫 Teacher Page** — Register, search, and update teachers.  
- **📚 Course Page** — Add courses and lessons to them.  
- **📋 Roster Page** — View daily schedule & student check-in.  
- **💰 Finance Page** — Record and view student payments

---

## 📟 User Interface

![User Interface](image.png)

- Built with **Streamlit** components:
  - `st.form()` for input and actions  
  - `st.data_editor()` for interactive tables with row selection  
  - `st.dataframe()` and `st.table()` for displaying structured data  

### Example Workflows

- **Home Page**:
![Home Page](image-2.png)


- **Course Management**:  
  - Select teacher and assign them to a new course.  
  - Add lessons (day, time, room) into existing courses.
  ![Course Page](image-3.png)

- **Roster Page**:  
  - Choose a day and view all lessons scheduled.  
  - Check-in students into classes.  
  ![Roaster Page](image-1.png)

- **Student Page**:  
  - Search student by ID or name.  
  - Register new students.  
  - Enroll or switch courses.  
  ![Student Page 1](image-4.png)
  ![Student Page 2](image-5.png)

- **Teacher Page**:  
  - Search teachers.  
  - Register new teachers.  
  - Update existing teacher info.  

- **Finance Page**
- Record New Payment:  
  - Select a student from a dropdown.  
  - Enter payment amount and method (e.g., Cash, Credit Card).  
  - Automatically saves transaction persistently.  
  ![Finance Page](image-7.png)

- View Payment History:  
  - Choose a student to view all recorded payments.  
  - Displays transactions in a clean `pandas` DataFrame. 
  ![Finance Page](image-6.png)

---

## 💡 Design Choices
1. **Streamlit GUI** for usability (replaces terminal menus).  
2. **OOP architecture** kept for clean separation of data handling vs UI.  
3. **Session state & selection tables** used for interactive workflows.  
4. **Backend untouched** — GUI adapts to return either single or multiple results.  
5. **Expandability** — New features (switch courses, check-in) are modular.  

---

## 🚀 How to Run
1. Ensure **Python 3.x** is installed.  
2. Save all code in the project folder.  
3. Install requirements:
   ```bash
   pip install streamlit pandas

4. Run the main script:  
   ```bash
    python main.py

## 📬 Contact
Created by `WONG KAI HENG`  
GitHub: [Wong Kai Heng](https://github.com/WongKH1010)  
Email: kwon0175@student.monash.edu