import sqlite3
import re
import uuid


# ============================================================
# DATABASE STATUS
# ============================================================

# app.py checks this variable to display Online/Offline status.
# We are using SQLite locally.
supabase = True


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():
    conn = sqlite3.connect("student_records_directory.db")
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

conn = get_db_connection()

conn.execute("""
CREATE TABLE IF NOT EXISTS student_data (
    id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    roll_number TEXT NOT NULL,
    department TEXT NOT NULL,
    year TEXT NOT NULL,
    semester TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    college TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    normalized_roll_number TEXT NOT NULL,
    normalized_email TEXT NOT NULL,
    normalized_phone TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS redundancy_logs (
    id TEXT PRIMARY KEY,
    attempted_name TEXT NOT NULL,
    attempted_roll_number TEXT NOT NULL,
    attempted_department TEXT NOT NULL,
    attempted_year TEXT NOT NULL,
    attempted_semester TEXT NOT NULL,
    attempted_email TEXT NOT NULL,
    attempted_phone TEXT NOT NULL,
    attempted_college TEXT NOT NULL,
    classification_type TEXT NOT NULL,
    action_taken TEXT NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
)
""")

conn.commit()
conn.close()


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text: str) -> str:
    if not text:
        return ""

    cleaned = text.strip().lower()

    return re.sub(r"\s+", " ", cleaned)


# ============================================================
# NORMALIZE PHONE NUMBER
# ============================================================

def normalize_phone_number(phone: str) -> str:
    if not phone:
        return ""

    return re.sub(r"\D", "", phone)


# ============================================================
# NORMALIZE ROLL NUMBER
# ============================================================

def normalize_roll_number(roll_number: str) -> str:
    if not roll_number:
        return ""

    cleaned = roll_number.strip().upper()

    return re.sub(r"\s+", "", cleaned)


# ============================================================
# CHECK FOR DUPLICATE / REDUNDANT STUDENT
# ============================================================

def check_for_redundancy(
    full_name: str,
    roll_number: str,
    email: str,
    phone: str
):
    normalized_name = normalize_text(full_name)
    normalized_roll = normalize_roll_number(roll_number)
    normalized_email = normalize_text(email)
    normalized_phone = normalize_phone_number(phone)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM student_data
        WHERE normalized_roll_number = ?
           OR normalized_email = ?
           OR normalized_phone = ?
    """, (
        normalized_roll,
        normalized_email,
        normalized_phone
    ))

    records = cursor.fetchall()

    conn.close()

    if not records:
        return False, "Unique Record"

    for record in records:

        # Exact duplicate
        if (
            record["normalized_name"] == normalized_name
            and record["normalized_roll_number"] == normalized_roll
            and record["normalized_email"] == normalized_email
            and record["normalized_phone"] == normalized_phone
        ):
            return True, "Exact Duplicate"

        # Same roll number
        if record["normalized_roll_number"] == normalized_roll:
            return True, "Potential Match - Same Roll Number"

        # Same email
        if record["normalized_email"] == normalized_email:
            return True, "Potential Match - Same Email"

        # Same phone
        if record["normalized_phone"] == normalized_phone:
            return True, "Potential Match - Same Phone Number"

    return False, "Unique Record"


# ============================================================
# INSERT UNIQUE STUDENT
# ============================================================

def insert_unique_student(
    full_name: str,
    roll_number: str,
    department: str,
    year: str,
    semester: str,
    email: str,
    phone: str,
    college: str
):
    # Check that every field has a value
    if not all([
        full_name,
        roll_number,
        department,
        year,
        semester,
        email,
        phone,
        college
    ]):
        return {
            "status": "error",
            "message": "All student fields are required."
        }

    # Check for redundancy
    is_duplicate, classification = check_for_redundancy(
        full_name,
        roll_number,
        email,
        phone
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    # ========================================================
    # BLOCK DUPLICATE
    # ========================================================

    if is_duplicate:

        cursor.execute("""
            INSERT INTO redundancy_logs (
                id,
                attempted_name,
                attempted_roll_number,
                attempted_department,
                attempted_year,
                attempted_semester,
                attempted_email,
                attempted_phone,
                attempted_college,
                classification_type,
                action_taken
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            full_name,
            roll_number,
            department,
            year,
            semester,
            email,
            phone,
            college,
            classification,
            "Blocked"
        ))

        conn.commit()
        conn.close()

        return {
            "status": "duplicate",
            "message": (
                "Insertion blocked: This student record "
                f"matches an existing record ({classification})."
            )
        }

    # ========================================================
    # NORMALIZE DATA
    # ========================================================

    normalized_name = normalize_text(full_name)
    normalized_roll = normalize_roll_number(roll_number)
    normalized_email = normalize_text(email)
    normalized_phone = normalize_phone_number(phone)

    # ========================================================
    # INSERT NEW STUDENT
    # ========================================================

    try:

        cursor.execute("""
            INSERT INTO student_data (
                id,
                full_name,
                roll_number,
                department,
                year,
                semester,
                email,
                phone,
                college,
                normalized_name,
                normalized_roll_number,
                normalized_email,
                normalized_phone
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            full_name,
            roll_number,
            department,
            year,
            semester,
            email,
            phone,
            college,
            normalized_name,
            normalized_roll,
            normalized_email,
            normalized_phone
        ))

        conn.commit()
        conn.close()

        return {
            "status": "success",
            "message": "Student record successfully stored in the database."
        }

    except Exception as e:

        conn.rollback()
        conn.close()

        return {
            "status": "error",
            "message": f"Database insertion failure: {str(e)}"
        }


# ============================================================
# FETCH ALL STUDENTS
# ============================================================

def fetch_all_students():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM student_data
        ORDER BY created_at DESC
    """)

    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return rows


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================

# Your existing app.py was calling fetch_all_records().
# This keeps that old function working.

def fetch_all_records():

    return fetch_all_students()


# ============================================================
# FETCH AUDIT / REDUNDANCY LOGS
# ============================================================

def fetch_audit_logs():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM redundancy_logs
        ORDER BY processed_at DESC
    """)

    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return rows