from db import get_connection
import re

valid_vaccines = ['AF', 'BV', 'CZ', 'DM', 'EC']

vaccine_rules = {
    'AF': {'doses': 2, 'min_age': 12, 'max_age': None},
    'BV': {'doses': 2, 'min_age': 18, 'max_age': None},
    'CZ': {'doses': 2, 'min_age': 12, 'max_age': 45},
    'DM': {'doses': 2, 'min_age': 12, 'max_age': None},
    'EC': {'doses': 1, 'min_age': 18, 'max_age': None},
}

def is_valid_name(name):
    return re.match(r"^[A-Za-z\s\-']{2,}$", name)

# Validates that age is a digit and within a realistic human age range (1–119).
def is_valid_age(age):
    return age.isdigit() and 12 <= int(age) < 120

def is_valid_vaccination_center(vc):
    return vc.upper() in ['VC1', 'VC2']

def is_vaccine_eligible(vaccine, age):
    rule = vaccine_rules.get(vaccine)
    if not rule:
        return False
    min_age = rule['min_age']
    max_age = rule['max_age']
    return age >= min_age and (max_age is None or age <= max_age)

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
    vc = input("Enter Vaccination Center (VC1 or VC2 only): ").strip().upper()
    while not is_valid_vaccination_center(vc):
        print("❌ Invalid vaccination center. Only VC1 or VC2 are accepted.")
        vc = input("Enter Vaccination Center (VC1 or VC2 only): ").strip().upper()

    name = input("Enter Full Name: ").strip()
    while not is_valid_name(name):
        print("Invalid name. Use letters only (min 2 characters).")
        name = input("Enter Full Name: ").strip()

    age = input("Enter Age: ").strip()
    while not is_valid_age(age):
        print("❌ Invalid age. Only 12 to 119 years old are eligible for vaccination.")
        age = input("Enter Age: ").strip()
    age = int(age)  # ✅ Convert to integer right after validation

    print("Eligible Vaccines:\nAF, BV, CZ, DM (2 doses), or EC (1 dose)")
    vaccine = input("Select vaccine: ").strip().upper()
    while vaccine not in valid_vaccines:
        print("Invalid vaccine code. Choose from: AF, BV, CZ, DM, EC")
        vaccine = input("Select vaccine: ").strip().upper()

    while not is_vaccine_eligible(vaccine, age):
        print(f"❌ The selected vaccine '{vaccine}' is not suitable for age {age}. Please choose again.")
        vaccine = input("Select vaccine: ").strip().upper()
        while vaccine not in valid_vaccines:
            print("Invalid vaccine code. Choose from: AF, BV, CZ, DM, EC")
            vaccine = input("Select vaccine: ").strip().upper()

    # Validate contact early
    contact = input("Enter Contact Number: ").strip()
    while not is_valid_contact(contact):
        print("Invalid contact number. Please enter 10-15 digits only.")
        contact = input("Enter Contact Number: ").strip()

    # Check for duplicates immediately after getting both contact and email
    if contact_exists(contact):
        print("❌ This contact number is already registered.")
        return

    # Validate email early
    email = input("Enter Email Address: ").strip()
    while not is_valid_email(email):
        print("Invalid email format.")
        email = input("Enter Email Address: ").strip()

    if email_exists(email):
        print("❌ This email is already registered.")
        return

    # Only save if all validations pass and patient is new
    pid = save_patient(name, age, contact, email, vaccine, vc)
    print(f"✅ Patient registered successfully with ID: {pid}")

