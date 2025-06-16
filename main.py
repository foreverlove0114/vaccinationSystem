# main.py
# Import the features of the system as functions from respective modules.
from patient import register_patient
from vaccine import administer_vaccine
from search import show_patient_status
from stats import show_statistics

# The main() function displays the menu and handles user interaction.
def main():
    while True:
        print("\n=== Vaccination Management System ===")
        print("1. Register New Patient")
        print("2. Administer Vaccine")
        print("3. Search Patient Record & Status")
        print("4. Show Statistics by VC")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            register_patient()
        elif choice == '2':
            administer_vaccine()
        elif choice == '3':
            show_patient_status()
        elif choice == '4':
            show_statistics()
        elif choice == '5':
            break
        else:
            print("Invalid option. Try again.")

# Start the program by calling main() only if this file is executed directly.
if __name__ == "__main__":
    main()

#hello