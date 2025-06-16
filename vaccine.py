# vaccine.py
from db import get_connection
from datetime import datetime, timedelta

# Records a vaccination dose in the database with the current date.
def record_vaccination(patient_id, dose):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO vaccinations (patient_id, dose, date) VALUES (%s, %s, %s)"
    cursor.execute(sql, (patient_id, dose, datetime.now().date()))
    conn.commit()
    conn.close()

# Interface to administer a vaccine dose to a patient.
# Accepts either D1 or D2 and stores the information in the vaccinations table.
def administer_vaccine():
    pid = int(input("Enter Patient ID: "))
    dose = input("Enter Dose (D1/D2): ").upper()

    if dose == "D1":
        print("Dose 1 recorded. Advise patient to return in 4 weeks for Dose 2 (if required).")
    elif dose == "D2":
        print("Dose 2 recorded. Patient has completed vaccination.")
    else:
        print("Invalid dose input.")
        return

    record_vaccination(pid, dose)
    print(f"Dose {dose} recorded for patient {pid}.")
