from db import get_connection
import re


# Validates that age is a digit and within a realistic human age range (1–119).
def is_valid_age(age):
    return age.isdigit() and 0 < int(age) < 120

# Validates contact number to ensure it contains only digits and has a length between 10 and 15.
def is_valid_contact(contact):
    return re.match(r'^[0-9]{10,15}$', contact)

# Validates email using a basic regex pattern.
def is_valid_email(email):
    return re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email)

# Checks whether a patient already exists in the database using their contact number or email.
def patient_exists(contact, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE contact = %s OR email = %s", (contact, email))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None


# Saves a new patient record into the patients table and returns the generated patient ID.
def save_patient(name, age, contact, email, vaccine, vc):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO patients (name, age, contact, email, vaccine, vc)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (name, age, contact, email, vaccine, vc))
    conn.commit()
    pid = cursor.lastrowid
    cursor.close()
    conn.close()
    return pid

# Handles the full process of registering a new patient:
# 1. Collects user input with validation
# 2. Checks for duplicate contact/email
# 3. Saves valid records to the database
def register_patient():
    print("=== Register New Patient ===")
    vc = input("Enter Vaccination Center (e.g., VC1): ").strip()
    name = input("Enter Full Name: ").strip()

    age = input("Enter Age: ").strip()
    while not is_valid_age(age):
        print("Invalid age. Please enter a number between 1 and 120.")
        age = input("Enter Age: ").strip()

    age = int(age)

    print("Eligible Vaccines:")
    print("AF, BV, CZ, DM (2 doses), or EC (1 dose)")
    vaccine = input("Select vaccine: ").strip().upper()

    contact = input("Enter Contact Number: ").strip()
    while not is_valid_contact(contact):
        print("Invalid contact number. Please enter 10-15 digits only.")
        contact = input("Enter Contact Number: ").strip()

    email = input("Enter Email Address: ").strip()
    while not is_valid_email(email):
        print("Invalid email format.")
        email = input("Enter Email Address: ").strip()

    if patient_exists(contact, email):
        print("Patient already registered with the same contact or email.")
        return

    pid = save_patient(name, age, contact, email, vaccine, vc)
    print(f"Patient registered successfully with ID: {pid}")
