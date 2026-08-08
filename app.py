import streamlit as st
import pandas as pd
import database
import config


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Data Redundancy Removal System",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🎓 Student Data Redundancy Removal System")

st.caption(
    f"CodeAlpha Cloud Computing Internship — Task 1 Portfolio Project | "
    f"Developer: {config.DEVELOPER_NAME}"
)

st.write("---")


# ============================================================
# GET DATABASE DATA
# ============================================================

unique_records = database.fetch_all_students()
audit_logs = database.fetch_audit_logs()


# ============================================================
# DASHBOARD
# ============================================================

total_students = len(unique_records)
total_blocked = len(audit_logs)

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.metric(
        "Total Unique Students",
        total_students
    )

with col_b:
    st.metric(
        "Blocked Duplicate Attempts",
        total_blocked
    )

with col_c:
    if database.supabase:
        st.metric(
            "Database Status",
            "Online"
        )
    else:
        st.metric(
            "Database Status",
            "Offline"
        )


st.write("---")


# ============================================================
# MAIN COLUMNS
# ============================================================

left_column, right_column = st.columns(2)


# ============================================================
# STUDENT REGISTRATION FORM
# ============================================================

with left_column:

    st.subheader("🎓 Student Registration")

    with st.form("student_registration_form"):

        student_name = st.text_input(
            "Student Full Name",
            placeholder="e.g. Arunima Sadhukhan"
        )

        roll_number = st.text_input(
            "Roll Number",
            placeholder="e.g. ECE2026001"
        )

        department = st.text_input(
            "Department",
            placeholder="e.g. Electronics and Communication Engineering"
        )

        year = st.selectbox(
            "Academic Year",
            [
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year"
            ]
        )

        semester = st.selectbox(
            "Semester",
            [
                "1st Semester",
                "2nd Semester",
                "3rd Semester",
                "4th Semester",
                "5th Semester",
                "6th Semester",
                "7th Semester",
                "8th Semester"
            ]
        )

        email = st.text_input(
            "Email Address",
            placeholder="e.g. student@gmail.com"
        )

        phone = st.text_input(
            "Phone Number",
            placeholder="e.g. +91 9876543210"
        )

        college = st.text_input(
            "College / Institute",
            placeholder="e.g. Guru Nanak Institute of Technology"
        )

        submit_button = st.form_submit_button(
            "Validate & Store Student"
        )


        # ====================================================
        # SUBMIT STUDENT
        # ====================================================

        if submit_button:

            if (
                not student_name.strip()
                or not roll_number.strip()
                or not department.strip()
                or not email.strip()
                or not phone.strip()
                or not college.strip()
            ):

                st.error(
                    "Validation Failed: Please fill in all required fields."
                )

            else:

                with st.spinner(
                    "Checking student record for duplicates..."
                ):

                    result = database.insert_unique_student(
                        student_name,
                        roll_number,
                        department,
                        year,
                        semester,
                        email,
                        phone,
                        college
                    )


                if result["status"] == "success":

                    st.success(
                        result["message"]
                    )

                    st.rerun()


                elif result["status"] == "duplicate":

                    st.warning(
                        result["message"]
                    )


                else:

                    st.error(
                        result["message"]
                    )


# ============================================================
# DATABASE DISPLAY
# ============================================================

with right_column:

    database_tab, logs_tab = st.tabs(
        [
            "🗄️ Student Database",
            "🛡️ Duplicate Logs"
        ]
    )


    # ========================================================
    # STUDENT DATABASE
    # ========================================================

    with database_tab:

        st.write(
            "Unique student records stored in the database:"
        )

        if unique_records:

            students_df = pd.DataFrame(unique_records)

            students_df = students_df.rename(
                columns={
                    "full_name": "Student Name",
                    "roll_number": "Roll Number",
                    "department": "Department",
                    "year": "Year",
                    "semester": "Semester",
                    "email": "Email",
                    "phone": "Phone Number",
                    "college": "College",
                    "created_at": "Registered At"
                }
            )

            columns_to_remove = [
                "id",
                "normalized_name",
                "normalized_roll_number",
                "normalized_department",
                "normalized_year",
                "normalized_semester",
                "normalized_email",
                "normalized_phone",
                "normalized_college"
            ]

            students_df = students_df.drop(
                columns=columns_to_remove,
                errors="ignore"
            )

            st.dataframe(
                students_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No student records have been added yet."
            )


    # ========================================================
    # DUPLICATE LOGS
    # ========================================================

    with logs_tab:

        st.write(
            "Duplicate student records blocked by the system:"
        )

        if audit_logs:

            logs_df = pd.DataFrame(audit_logs)

            logs_df = logs_df.rename(
                columns={
                    "attempted_name": "Student Name",
                    "attempted_roll_number": "Roll Number",
                    "attempted_department": "Department",
                    "attempted_year": "Year",
                    "attempted_semester": "Semester",
                    "attempted_email": "Email",
                    "attempted_phone": "Phone Number",
                    "attempted_college": "College",
                    "classification_type": "Classification",
                    "action_taken": "System Action",
                    "processed_at": "Processed At"
                }
            )

            columns_to_remove = [
                "id"
            ]

            logs_df = logs_df.drop(
                columns=columns_to_remove,
                errors="ignore"
            )

            st.dataframe(
                logs_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No duplicate student records have been blocked yet."
            )