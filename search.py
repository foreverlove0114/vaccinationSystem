# search.py
from db import get_connection
from datetime import datetime, timedelta

# Rules for next dose interval
vaccine_rules = {
    'AF': {'interval': 14, 'doses': 2},
    'BV': {'interval': 21, 'doses': 2},
    'CZ': {'interval': 21, 'doses': 2},
    'DM': {'interval': 28, 'doses': 2},
    'EC': {'interval': 0, 'doses': 1},
}

def get_patient_info(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
    patient = cursor.fetchone()

    cursor.execute("SELECT * FROM vaccinations WHERE patient_id = %s ORDER BY date_administered ASC", (patient_id,))
    doses = cursor.fetchall()

    conn.close()
    return patient, doses

def show_patient_status():
    try:
        pid = int(input("Enter Patient ID to search: "))
    except ValueError:
        print("Invalid input. Please enter a numeric patient ID.")
        return

    patient, doses = get_patient_info(pid)

    if not patient:
        print("❌ Patient not found.")
        return

    print("\n=== Patient Details ===")
    print(f"ID: {patient['patient_id']}")
    print(f"Name: {patient['name']}")
    print(f"Age: {patient['age']}")
    print(f"Contact: {patient['contact']}")
    print(f"Email: {patient['email']}")
    print(f"Vaccination Center: {patient['vc']}")
    print(f"Vaccine: {patient['vaccine']}")
    print("\n--- Vaccination History ---")

    if not doses:
        print("No doses recorded.")
    else:
        for dose in doses:
            print(f"Dose: {dose['dose']} | Date: {dose['date_administered']}")

    # Determine status and suggest next dose date if applicable
    vaccine = patient['vaccine']
    total_doses_required = vaccine_rules[vaccine]['doses']
    interval_days = vaccine_rules[vaccine]['interval']

    if len(doses) == 0:
        print("\nStatus: NEW")
    elif len(doses) == 1 and total_doses_required == 2:
        print("Status: COMPLETED-D1")
        first_dose_date = doses[0]['date_administered']
        next_dose_date = first_dose_date + timedelta(days=interval_days)
        print(f"💡 Suggest patient to return for Dose 2 on: {next_dose_date}")
    else:
        print("Status: COMPLETED")

    print("\n===========================")
