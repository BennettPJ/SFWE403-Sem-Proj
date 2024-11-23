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

### **Reports**
Generated reports are saved here:
- `Financial_Report_*.csv`: Financial summaries.
- `Inventory_Report_*.csv`: Inventory status reports.
- `User_Transactions_Report_*.csv`: Tracks user activity within the system.

---

### **Resources**
A collection of images and resources used in the application's UI:
- Icons such as `pharmacist.png`, `medicine.png`, `user.png`, etc.
- UI-related resources like `pharm.qrc`.

---

### **Tests**
Contains test scripts and data used for unit testing:
- **`Inventory_test`**: Unit tests for inventory management.
- **`Test_databases`**: Test databases for validation.
- `test_inventory.py`: Tests inventory logic.
- `test_login_roles.py`: Tests user authentication and roles.
- `test_purchase.py`: Validates purchase workflows.

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
- `Purchase.ui`: This display's the screen that allows pharmacy staff to enter in items a customer will want to purchase. This will also display a recipt for any item that was purchased by the user.
- `Reports.ui`: This display's different buttons that the user can interact with to generate different types of reports for different aspects of the system.
- `storeHours.ui`: This display's the screen that contains the store hours as well as a calendar and the time of day. The manager can change the store information from this UI as well.
- `template.ui`: This is a template page that the team worked off of. This has no functionality and was purely for team internal use.
- `UpdateCustomerInfo.ui`: This display's the UI that allows staff to update and add patients to the system.
  
---

### **logs**
Contains a master log file to store different actions that happen within the application
- `transaction.log`: This keeps track of logins, logouts, purchases, and other data. This file is used to track everything so reports can be built based on it.

---

### **src**
The source code for the application, organized by functionality:
- **Modules**:
  - `AdminUI.py`, `Dashboard.py`: User interfaces for admins and dashboards.
  - `Inventory.py`: Inventory management logic.
  - `LoginRoles.py`: User login and role management.
  - `Patient.py`: Manages patient-related data and interactions.
  - `Purchases.py`: Handles purchases.
  - `Reports.py`: Generates reports.
- **Utilities**:
  - `resources_rc.py`: PyQt resources.

---

## Features
1. **Inventory Management**: Manage stock levels and order medications.
2. **Patient Information**: Store and retrieve patient details securely.
3. **Prescription Processing**: Create, update, and manage prescriptions.
4. **Reporting**: Generate financial, inventory, and user transaction reports.
5. **User Authentication**: Secure login with role-based access control.
6. **Audit Logging**: Track all significant system activities for accountability.

---

## How to Run
1. Install the required dependencies:
    ```bash
    pip install PyQt5 fpdf
   
2. Clone the repository:
    ```bash
    git clone https://github.com/BennettPJ/SFWE403-Sem-Proj.git
    cd SFWE403-Sem-Proj
   
3. Run the main.py file:
    ```bash
    python main.py
