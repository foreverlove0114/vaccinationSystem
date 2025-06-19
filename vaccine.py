# vaccine.py
from db import get_connection
from datetime import datetime, timedelta

# Vaccine rules: dose count, interval between D1 and D2
vaccine_intervals = {
    'AF': 14,  # 2 weeks
    'BV': 21,  # 3 weeks
    'CZ': 21,  # 3 weeks
    'DM': 28,  # 4 weeks
    'EC': 0,   # Single dose
}

# Fetch patient data
def get_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()
    return patient

# Get existing doses for a patient
def get_doses(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT dose, date_administered FROM vaccinations WHERE patient_id = %s", (patient_id,))
    doses = cursor.fetchall()
    cursor.close()
    conn.close()
    return doses

# Records a vaccination dose in the database with the current date.
def record_vaccination(patient_id, dose):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO vaccinations (patient_id, dose, date_administered) VALUES (%s, %s, %s)"
    cursor.execute(sql, (patient_id, dose, datetime.now().date()))
    conn.commit()
    cursor.close()
    conn.close()


# Get patient's vaccine type and latest Dose 1 date
def get_patient_vaccine_info(patient_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT vaccine FROM patients WHERE patient_id = %s", (patient_id,))
    result = cursor.fetchone()
    vaccine = result[0] if result else None

    cursor.execute("""
        SELECT date_administered FROM vaccinations
        WHERE patient_id = %s AND dose = 'D1'
        ORDER BY date_administered DESC LIMIT 1
    """, (patient_id,))
    result = cursor.fetchone()
    dose1_date = result[0] if result else None

    cursor.close()
    conn.close()
    return vaccine, dose1_date


# Interface to administer a vaccine dose to a patient.
def administer_vaccine():
    try:
        pid = int(input("Enter Patient ID: "))
    except ValueError:
        print("❌ Invalid Patient ID. Must be a number.")
        return

    dose = input("Enter Dose (D1/D2): ").upper()
    if dose not in ['D1', 'D2']:
        print("❌ Invalid dose input. Please enter 'D1' or 'D2'.")
        return

    vaccine, dose1_date = get_patient_vaccine_info(pid)

    if not vaccine:
        print("❌ Patient not found.")
        return

    if dose == "D1":
        if vaccine == "EC":
            print("✅ EC is a single-dose vaccine. Administering now.")
        else:
            print(f"✅ Dose 1 recorded. Patient should return in {vaccine_intervals[vaccine]} days for Dose 2.")
        record_vaccination(pid, dose)

    elif dose == "D2":
        if vaccine == "EC":
            print("❌ EC is a single-dose vaccine. Dose 2 is not required.")
            return
        if not dose1_date:
            print("❌ Dose 1 has not been recorded for this patient.")
            return

        interval_required = vaccine_intervals.get(vaccine, 0)
        days_since_dose1 = (datetime.now().date() - dose1_date).days

        if days_since_dose1 < interval_required:
            print(f"❌ It's too early for Dose 2. Please return in {interval_required - days_since_dose1} day(s).")
            return

        print("✅ Dose 2 recorded. Patient has completed the vaccination.")
        record_vaccination(pid, dose)