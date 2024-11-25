# SFWE403 Semester Project Team 2
This repository houses the code for the SFWE 403 class project for team 2. The team consists of Amber Parker, Bennett Jackson, Chris Karceski, Jennifer Galvan Garcia, Minh Le, and Ruben Galdean. For more information on the projects structure and usage please review the below information. 


# Pharmacy Management System

## Overview
The Pharmacy Management System is a comprehensive application designed to handle the day-to-day operations of a pharmacy. It includes functionality for inventory management, patient management, prescription processing, reporting, and more. This project uses a combination of Python and PyQt5 for the UI, and CSV files as the database for lightweight, portable data storage.

## SLOCs:
This project contains roughly 59,223 lines of code.

---

## Project Structure

### High-Level project overview of file directories
. <br>
├── DBFiles               --> Contains CSV database files for persistent data storage <br>
├── Reports               --> Generated financial, inventory, and activity reports <br>
├── Resources             --> UI assets (icons, images, and resource files) <br>
├── Tests                 --> Unit tests and test databases <br>
├── UI                    --> PyQt .ui files for graphical interfaces <br>
├── logs                  --> System transaction logs <br>
├── src                   --> Main Source code for backend logic <br>
├── main.py               --> Application entry point <br>
└── README.md             --> Project documentation <br>

### **Root Directory**
- **`main.py`**  
  The main entry point of the application. This is the file that is ran to start the overall application. Once this is ran a new window will appear with the pharmacy management system active.

- **`README.md`**  
  This documentation file. All of the files and their functionalities are documented here.

---

### **DBFiles**
Contains all the CSV database files used to store persistent data for the application.
- `db_inventory.csv`: Holds all of the inventory data. This contains the headers -> Item,ID,Quantity,Price,Expiration Date,Date Added,Date Updated,Date Removed
- `db_patient_info.csv`: Holds all of the patient information entered into the system. This contains the headers -> FirstName,LastName,DateOfBirth,StreetAddress,City,State,ZipCode,PhoneNumber,Email,NameInsured,Provider,PolicyNumber,GroupNumber
- `db_pharmacy_info.csv`: This will only contain one row entry. This holds all of the pharmacies information. The headers are -> name,website,address,owner,phone_number,mon_hours,tue_hours,wed_hours,thu_hours,fri_hours,sat_hours,sun_hours
- `db_prescriptions.csv`: This stores all of the prescriptions that are entered into the system. This file also tracks if a prescription is filled, picked up, or pending. The headers are -> Patient_First_Name,Patient_Last_Name,Patient_DOB,Prescription_Number,Medication,Quantity,Status
- `db_purchase_data.csv`: This stores the purchase transaction records. The headers are -> Date,First Name,Last Name,Item Name,ID,Quantity,Price,Total Cost,Grand Total,Payment Method,Prescription
- `db_user_account.csv`: This stores authorized user information including usernames and passwords. The headers are -> Username,Email,Password,Role,Locked_counter,Locked_status

---

### **logs**
Contains a master log file to store different actions that happen within the application.
- `transaction.log`: This keeps track of logins, logouts, purchases, and other data. This file is used to track everything so reports can be built based on it.

---

### **Reports**
Generated reports are saved here:
- `Financial_Report_*.csv`: This is a CSV file that stores all of the financial data related to sales in the system. The date that takes place instead of the * is the date that the report was created on. This file is used for generating a PDF report to display to the user.
- `Financial_Report_Period_*.csv`: This file is a CSV file that holds all financial data related to sales for a set period of time determined by the user. This file is used to create a PDF report of that information.
- `Inventory_Report_*.csv`: This is a CSV file that stores all of the inventory data. The date that takes place instead of the * is the date that the report was created on. This file is used for generating a PDF report to display to the user.
- `Inventory_Report_Period_*.csv`: This file is a CSV file that holds all inventory data for a set period of time determined by the user. This file is used to create a PDF report of that information.
- `User_Transactions_Report_*.csv`: This file is a CSV file that tracks user logins and logouts. This file is used to create a PDF report of that information.

---

### **Resources**
A collection of images and resources used in the application's UI. All images are copyright free. All images were used to enhance the UI/UX of the application.
- `computer.png`: This is an image of a computer with a medication displayed on it.
- `consultation.png`: This is an image of a phone with a medication inside a text bubble.
- `floppy-disk.png`: This is a floppy disk which represents saving something within the system.
- `information.png`: This is an image of a medical help desk.
- `medicine.png`: This is a image of the medical symbol commonly seen in the medical field.
- `pharm.png`: This is an image of a pharmacist behind the pharmacy counter.
- `pharm.qrc`: This is an XML formatted file identifying the images used within this project.
- `pharmacist.png`: This is an image of the outline of a pharmacist.
- `pharmacy.png`: This is an image of medications.
- `prescription.png`: This is an image of a prescription form.
- `report.png`: This is an image of a report file with additional charts.
- `right.png`: This is an image with an arrow pointing to the right.
- `Screenshot 2024-10-02 201939.png`: This is an image of a pharmacist behind the pharmacy counter.
- `treatment.png`: This is an image of a hand holding a medical package.
- `user.png`: This is an image of a person next to a gear to represent user settings.
- `vaccine.png`: This is an image of a medical vaccine.

---

### **src**
The main source code for the backend of the pharmacy management system:
- **\_\_pycache\_\_**:
  - All files contained in here are compiles bytecode for all of the .py files listed below. This is used to speed up the execution of the application. 
- `AdminUI.py`: This file acts as the backend to the Admin fronted page. This file handles all the logic to allow store managers to manage user accounts. This includes locking and unlocking accounts, deleting users, changing passwords, and more.
- `CreateAccount.py`: This is the backend to the page that allows managers to create new accounts for the pharmacy management system. This handles password checking logic to ensure a password is valid as well as adding the new user account to the database.
- `Dashboard.py`: This is the backend that routes to all the different pages within the application. This also handles logic for the access control system ensuring certain user groups can only access pages they are allowed to access.
- `FillPrescriptionUI.py`: This handles all the backend logic for allowing a pharmacist to fill a prescription. Within this file it reads from the prescriptions database to populate the table with all the pending prescriptions. This backend file also interfaces with the inventory class to ensure that a medication being filled is in stock and not expired.
- `Inventory.py`: This is a helper file that contains a class for interacting with the inventory database. This includes functionality such as checking the stock for a medication, checking if a medication is expired, and more. This class is used in many backend files throughout the project.
- `InventoryUI.py`: This is the backed file for the inventory page. This file handles interactions between the inventory class and the frontend page based on user input.
- `LogInGUI.py`: This backend file handles the interface between the LoginRoles class and the frontend UI based on user input. This backend file also handles the page routing based on what page the user the user navigates to.
- `LoginRoles.py`: This is a helper class that handles the validation of users as well as the interaction between the user accounts database. Some of the functionality in this class is username and password validation, finding user accounts by username, the removal of users, and more.
- `Patient.py`: This file is a helper class that handles the interaction with the patient info database. This file contains functionality such as adding and removing patient, updating patient info, and looking up patient info by their name and date of birth.
- `PatientUI.py`: This backend file relies on the Patient helper class. This file handles the users input from the frontend and passes the data off to the helper patient class for database interaction. 
- `Prescriptions.py`: This is a helper class that handles all interactions with the prescriptions database. This includes functionality such as adding a prescription, updating a prescription's status, and looking up prescriptions by patient.
- `PrescriptionUI.py`: This file handles the interaction between the frontend and the Prescriptions helper class. This includes passing data between the frontend and the database class. This also handles displaying popups on the frontend to the user. 
- `Purchases.py`: This file handles the interaction between the frontend and the purchases database. This class also interfaces with the inventory helper class to ensure that the inventory display's accurate data. Additionally, this class handles displaying receipt popups as there is no physical hardware integrations. 
- `Reports.py`: This class handles making PDF files out of the logged system data. This also handles the interaction between the frontend and the popups allowing users to select a date range for their generated reports. 
- `resources_rc.py`: This is an auto-generated resource file by PyQt. This contains compiled resource object code. 
- `StoreHoursUI.py`: This file handles the transfer of data between the pharmacy info database and the frontend. This file also relies on the LoginRoles helper class to validate manager credentials for changing the information displayed on the page. 
- `StoreInfoManager.py`: This is a helper class that interacts with the pharmacy info database. This includes reading and writing to the CSV file database. This helper class is used in the StoreHoursUI file. 

---

### **Tests**
Contains test scripts and data used for unit testing. This is not comprehensive testing. Our main testing method was through the UI and print statements within the code. The following files were used for testing:
- **\_\_pycache\_\_**:
  - All files contained in here are compiles bytecode for all of the .py files listed below. This is used to speed up the execution of the application. 
- `Inventory_test`: A folder containing tests that pertained to the inventory class.
  - **\_\_pycache\_\_**:
    - All files contained in here are compiles bytecode for all of the .py files listed below. This is used to speed up the execution of the application. 
  - `test_inventory.py`: This was the original test for the inventory class. After large code updates this test no longer works as we switched to a new way of testing through the UI.
- `Test_databases`: A folder containing mock databases that were copies of the production databases.
  - All files contained in this directory were copies of the original databases. Each file is a CSV file that was used to test data storage and retrieval.
- `test_inventory.py`: A newer version of the previous inventory test. This has also been depreciated since moving to our new form of testing. The goal of this was to test the inventory helper class.
- `test_login_roles.py`: This was to test the LoginRoles helper class to ensure it interacted with the database properly.
- `test_purchase.py`: This was to test the purchases  class to ensure it interacted with the database properly as well as all other functionality worked as expected. This test has also been depreciated since moving onto our newer test strategy.

---

### **UI**
PyQt UI files for the graphical interface:
- `AdminUI.ui`: This display's the admin screen that can be found by navigating through the dashboard UI. This is where admins can update users passwords and lock/unlock users accounts.
- `createAccount.ui`: This display's the screen where a manager can create a new pharmacy staff account allowing the new user to login.
- `Dashboard.ui`: This display's the main dashboard that allows users to navigate to different pages. Each page within the dashboard provides the user with different functionalities that can be carried out.
- `FillPrescription.ui`: This display's the screen where pharmacists can fill any pending prescription that is in the system. This screen is blocked by access control only allowing pharmacists to view it.
- `Inventory.ui`: This display's the UI that allows users to manage the inventory that is linked to the pharmacy management system.
- `LogInGUI.ui`: This display's the page that the user is greeted with when opening the pharmacy management system application. The user will login on this page. This page also allows all users to view store hours and managers to create accounts.
- `PendingPrescription.ui`: This display's the prescription management page. Here pharmacy staff can enter in new prescriptions, mark prescriptions as picked up, and search for prescriptions by patient.
- `Purchase.ui`: This display's the screen that allows pharmacy staff to enter in items a customer will want to purchase. This will also display a receipt for any item that was purchased by the user.
- `Reports.ui`: This display's different buttons that the user can interact with to generate different types of reports for different aspects of the system.
- `storeHours.ui`: This display's the screen that contains the store hours as well as a calendar and the time of day. The manager can change the store information from this UI as well.
- `template.ui`: This is a template page that the team worked off of. This has no functionality and was purely for team internal use.
- `UpdateCustomerInfo.ui`: This display's the UI that allows staff to update and add patients to the system.

---

## How to Run
1. Install Anaconda and setup the environment:
   - Follow this link to learn more about how to setup and install Anaconda: https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html
  
2. Install the required dependencies:
    ```bash
    pip install PyQt5 fpdf pandas
   
3. Clone the repository:
    ```bash
    git clone https://github.com/BennettPJ/SFWE403-Sem-Proj.git
    cd SFWE403-Sem-Proj
   
4. Run the main.py file:
    ```bash
    python main.py
