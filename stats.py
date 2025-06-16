# stats.py
from db import get_connection

# Fetches and displays statistics for each vaccination center (VC),
# including total registered patients, completed vaccinations, and pending second doses.
def show_statistics():
    conn = get_connection()
    cursor = conn.cursor()

    # Get list of unique vaccination centers
    cursor.execute("SELECT vc FROM patients")
    all_vcs = set(vc[0] for vc in cursor.fetchall())

    for vc in all_vcs:
        cursor.execute("""
            SELECT p.patient_id, COUNT(v.dose) as dose_count 
            FROM patients p 
            LEFT JOIN vaccinations v ON p.patient_id = v.patient_id 
            WHERE p.vc = %s 
            GROUP BY p.patient_id
        """, (vc,))
        rows = cursor.fetchall()
        total = len(rows)
        completed = sum(1 for r in rows if r[1] == 2 or (r[1] == 1 and get_vaccine_type(r[0]) == 'EC'))
        pending = total - completed


        # Display stats for each VC
        print(f"\nVC: {vc}")
        print(f"Total Patients: {total}")
        print(f"Completed Vaccination: {completed}")
        print(f"Waiting for Dose 2: {pending}")

    conn.close()

# Helper function to get the vaccine type of a patient
def get_vaccine_type(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT vaccine FROM patients WHERE patient_id = %s", (patient_id,))
    vaccine = cursor.fetchone()
    conn.close()
    return vaccine[0] if vaccine else None
