# search.py
from db import get_connection

# Retrieves full patient record and vaccination doses from the database.
def get_patient_info(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
    patient = cursor.fetchone()

    cursor.execute("SELECT * FROM vaccinations WHERE patient_id = %s", (patient_id,))
    doses = cursor.fetchall()
    conn.close()

    return patient, doses

# Allows the user to search for a patient by ID and view:
# - Personal info
# - Vaccination doses received
# - Current vaccination status (NEW, COMPLETED, COMPLETED-D1)
def show_patient_status():
    pid = int(input("Enter Patient ID to search: "))
    patient, doses = get_patient_info(pid)

    if not patient:
        print("Patient not found.")
        return

    print(f"Patient ID: {patient['patient_id']}")
    print(f"VC: {patient['vc']}, Age: {patient['age']}, Vaccine: {patient['vaccine']}, Contact: {patient['contact']}")
    print(f"Doses Given: {[dose['dose'] for dose in doses]}")

    vaccine = patient['vaccine']
    if vaccine == 'EC':
        if doses:
            print("Status: COMPLETED")
        else:
            print("Status: NEW")
    else:
        if not doses:
            print("Status: NEW")
        elif len(doses) == 1:
            print("Status: COMPLETED-D1")
        else:
            print("Status: COMPLETED")
