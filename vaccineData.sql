#######################################################################################
# Create Table
#######################################################################################
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    contact VARCHAR(100),
    email VARCHAR(100),
    vc VARCHAR(10),
    vaccine VARCHAR(10)
);

CREATE TABLE vaccinations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    dose VARCHAR(2),  -- 'D1' or 'D2'
    date_administered DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

#######################################################################################
# Drop Table
#######################################################################################
DROP TABLE IF EXISTS vaccinations;
DROP TABLE IF EXISTS patients;

#######################################################################################
# Constraint the data input as unique
#######################################################################################
ALTER TABLE patients
ADD CONSTRAINT unique_patient_info
UNIQUE (contact, email);

CREATE USER 'vaxuser'@'localhost' IDENTIFIED BY 'vaxpass123';
GRANT ALL PRIVILEGES ON vaccination_system.* TO 'vaxuser'@'localhost';
FLUSH PRIVILEGES;

SELECT * FROM PATIENTS;





