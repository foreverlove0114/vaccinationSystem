from db import get_connection
import re

valid_vaccines = ['AF', 'BV', 'CZ', 'DM', 'EC']

def is_valid_name(name):
    return re.match(r"^[A-Za-z\s\-']{2,}$", name)

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
def contact_exists(contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM patients WHERE contact = %s", (contact,))
    exists = cursor.fetchall()  # read all results to clear buffer
    cursor.close()
    conn.close()
    return len(exists) > 0

def email_exists(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM patients WHERE email = %s", (email,))
    exists = cursor.fetchall()  # read all results to clear buffer
    cursor.close()
    conn.close()
    return len(exists) > 0


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
    while not is_valid_name(name):
        print("Invalid name. Use letters only (min 2 characters).")
        name = input("Enter Full Name: ").strip()

    age = input("Enter Age: ").strip()
    while not is_valid_age(age):
        print("Invalid age. Please enter a number between 1 and 120.")
        age = input("Enter Age: ").strip()
    age = int(age)

    print("Eligible Vaccines:\nAF, BV, CZ, DM (2 doses), or EC (1 dose)")
    vaccine = input("Select vaccine: ").strip().upper()
    while vaccine not in valid_vaccines:
        print("Invalid vaccine code. Choose from: AF, BV, CZ, DM, EC")
        vaccine = input("Select vaccine: ").strip().upper()

    # Validate contact early
    contact = input("Enter Contact Number: ").strip()
    while not is_valid_contact(contact):
        print("Invalid contact number. Please enter 10-15 digits only.")
        contact = input("Enter Contact Number: ").strip()

    # Validate email early
    email = input("Enter Email Address: ").strip()
    while not is_valid_email(email):
        print("Invalid email format.")
        email = input("Enter Email Address: ").strip()

    # Check for duplicates immediately after getting both contact and email
    if contact_exists(contact):
        print("❌ This contact number is already registered.")
        return
    if email_exists(email):
        print("❌ This email is already registered.")
        return

    # Only save if all validations pass and patient is new
    pid = save_patient(name, age, contact, email, vaccine, vc)
    print(f"✅ Patient registered successfully with ID: {pid}")

