# SFWE403 Semester Project Team 2
This repository houses the code for the SFWE 403 class project for team 2. The team consists of Amber Parker, Bennett Jackson, Chris Karceski, Jennifer Galvan Garcia, Minh Le, and Ruben Galdean. For more information on the projects structure and usage please review the below information. 


# Pharmacy Management System

## Overview
The Pharmacy Management System is a comprehensive application designed to handle the day-to-day operations of a pharmacy. It includes functionality for inventory management, patient management, prescription processing, reporting, and more. This project uses a combination of Python and PyQt5 for the UI, and CSV files as the database for lightweight, portable data storage.

## SLOCs:
This project contains roughly 59,223 lines of code.

---

## Project Structure

### High-Level project overview
. <br>
├── DBFiles               --> Contains CSV database files for persistent data storage <br>
├── Reports               --> Generated financial, inventory, and activity reports <br>
├── Resources             --> UI assets (icons, images, and resource files) <br>
├── Tests                 --> Unit tests and test databases <br>
├── UI                    --> PyQt .ui files for graphical interfaces <br>
├── logs                  --> System transaction logs <br>
├── src                   --> Main Source code for backend logic <br>
│</t> ├── AdminUI.py        --> AdminUI backend <br>
│</t> ├── Inventory.py      --> Inventory management backend <br>
│</t> ├── Patient.py        --> Patient management backend <br>
│</t> ├── Reports.py        --> Report generation backend <br>
│</t> └── …                 --> Other backend files <br>
├── main.py               --> Application entry point <br>
└── README.md             --> Project documentation <br>

### **Root Directory**
- **`main.py`**  
  The main entry point of the application. This is the file that is ran to start the overall application. Once this is ran a new window will appear with the pharmacy management system active.

- **`README.md`**  
  This documentation file. All of the files and their functionalities are documented here.

---

### **DBFiles**
Contains the CSV database files used to store persistent data for the application.
- `db_activity_log.csv`: Logs system activities.
- `db_inventory.csv`: Tracks inventory data.
- `db_inventory_activity_log.csv`: Logs inventory operations.
- `db_patient_info.csv`: Stores patient information.
- `db_pharmacy_info.csv`: Pharmacy details.
- `db_prescriptions.csv`: Stores prescription data.
- `db_purchase_data.csv`: Purchase transaction records.
- `db_user_account.csv`: User account details.
- `purchase.csv`: Records specific purchase actions.

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
- `AdminUI.ui`: Admin panel.
- `Dashboard.ui`: Main dashboard.
- `Inventory.ui`: Inventory management.
- `LogInGUI.ui`: Login screen.
- `Purchase.ui`: Purchase screen.

---

### **logs**
- `transaction.log`: A log file that tracks all system transactions.

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
