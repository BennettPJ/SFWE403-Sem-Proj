# SFWE403-Sem-Proj
This will be a repository to hold the teams SFWE 403 source code for the semester project



# Project Directory Structure:
.<br>
├── DBFiles <br>
│   ├── db_activity_log.csv <br>
│   ├── db_inventory.csv <br>
│   ├── db_inventory_activity_log.csv <br>
│   ├── db_patient_info.csv <br>
│   ├── db_pharmacy_info.csv <br>
│   ├── db_prescriptions.csv <br>
│   ├── db_purchase_data.csv <br>
│   ├── db_user_account.csv <br>
│   └── purchase.csv <br>
├── README.md <br>
├── Reports <br>
│   ├── Financial_Report_2024-11-10.csv <br>
│   ├── Financial_Report_Period_2024-11-10.csv <br>
│   ├── Inventory_Report_2024-11-10.csv <br>
│   ├── Inventory_Report_Period_2024-11-10.csv <br>
│   └── User_Transactions_Report_2024-11-10.csv <br>
├── Resources <br>
│   ├── Pharmacies-in-Portsmouth-and-Southsea.jpg <br>
│   ├── Pharmacology.jpg <br>
│   ├── Screenshot 2024-10-02 201939.png <br>
│   ├── computer.png <br>
│   ├── consultation.png <br>
│   ├── floppy-disk.png <br>
│   ├── information.png <br>
│   ├── medicine.png <br>
│   ├── pharm.png <br>
│   ├── pharm.qrc <br>
│   ├── pharmacist.png <br>
│   ├── pharmacy.png <br>
│   ├── prescription.png <br>
│   ├── report.png <br>
│   ├── right.png <br>
│   ├── treatment.png <br>
│   ├── user.png <br>
│   └── vaccine.png <br>
├── Tests <br>
│   ├── Inventory_test <br>
│   │   ├── __pycache__ <br>
│   │   │   └── test_inventory.cpython-310.pyc <br>
│   │   └── test_inventory.py <br>
│   ├── Test_databases <br>
│   │   ├── test_db_filled_Prescriptions.csv <br>
│   │   ├── test_db_inventory.csv <br>
│   │   ├── test_db_picked_up_prescriptions.csv <br>
│   │   ├── test_db_user_account.csv <br>
│   │   ├── test_pharmacy_info.csv <br>
│   │   └── test_purchases.csv <br>
│   ├── __pycache__ <br>
│   │   ├── test_inventory.cpython-310-pytest-7.4.4.pyc <br>
│   │   ├── test_inventory.cpython-310.pyc <br>
│   │   ├── test_inventory.cpython-312.pyc <br>
│   │   ├── test_login_roles.cpython-310-pytest-7.4.4.pyc <br>
│   │   ├── test_login_roles.cpython-310.pyc <br>
│   │   ├── test_login_roles.cpython-312.pyc <br>
│   │   ├── test_pharmacy_info.cpython-310-pytest-7.4.4.pyc <br>
│   │   ├── test_pharmacy_info.cpython-310.pyc <br>
│   │   ├── test_pharmacy_info.cpython-312.pyc <br>
│   │   ├── test_purchase.cpython-310-pytest-7.4.4.pyc <br>
│   │   ├── test_purchase.cpython-310.pyc <br>
│   │   └── test_purchase.cpython-312.pyc <br>
│   ├── test_inventory.py <br>
│   ├── test_login_roles.py <br>
│   ├── test_pharmacy_info.py <br>
│   └── test_purchase.py <br>
├── UI <br>
│   ├── AdminUI.ui <br>
│   ├── Dashboard.ui <br>
│   ├── FillPrescription.ui <br>
│   ├── Inventory.ui <br>
│   ├── LogInGUI.ui <br>
│   ├── OrderMedication.ui <br>
│   ├── PendingPrescription.ui <br>
│   ├── Purchase.ui <br>
│   ├── Reports.ui <br>
│   ├── UpdateCustomerInfo.ui <br>
│   ├── bennett-test.ui <br>
│   ├── createAccount.ui <br>
│   ├── storeHours.ui <br>
│   └── template.ui <br>
├── logs <br>
│   └── transaction.log <br>
├── main.py <br>
└── src <br>
    ├── AdminUI.py <br>
    ├── CreateAccount.py <br>
    ├── DBFiles <br>
    ├── Dashboard.py <br>
    ├── FillPrescriptionUI.py <br>
    ├── Inventory.py <br>
    ├── InventoryUI.py <br>
    ├── LogInGUI.py <br>
    ├── LoginRoles.py <br>
    ├── Patient.py <br>
    ├── PatientUI.py <br>
    ├── PrescriptionUI.py <br>
    ├── Prescriptions.py <br>
    ├── Purchases.py <br>
    ├── Reports.py <br>
    ├── StoreHoursUI.py <br>
    ├── StoreInfoManager.py <br>
    ├── __pycache__ <br>
    │   ├── AdminUI.cpython-310.pyc <br>
    │   ├── CreateAccount.cpython-310.pyc <br>
    │   ├── CustomerInfo.cpython-310.pyc <br>
    │   ├── Dashboard.cpython-310.pyc <br>
    │   ├── FillPrescription.cpython-310.pyc <br>
    │   ├── FillPrescriptionUI.cpython-310.pyc <br>
    │   ├── Inventory.cpython-310.pyc <br>
    │   ├── InventoryUI.cpython-310.pyc <br>
    │   ├── Inventory_db.cpython-310.pyc <br>
    │   ├── LogInGUI.cpython-310.pyc <br>
    │   ├── LoginRoles.cpython-310.pyc <br>
    │   ├── Login_roles.cpython-310.pyc <br>
    │   ├── OrderMedication.cpython-310.pyc <br>
    │   ├── Patient.cpython-310.pyc <br>
    │   ├── PatientUI.cpython-310.pyc <br>
    │   ├── PendingPrescriptionUI.cpython-310.pyc <br>
    │   ├── PendingPrescriptions.cpython-310.pyc <br>
    │   ├── PrescriptionUI.cpython-310.pyc <br>
    │   ├── Prescriptions.cpython-310.pyc <br>
    │   ├── Purchases.cpython-310.pyc <br>
    │   ├── Reports.cpython-310.pyc <br>
    │   ├── StoreHoursUI.cpython-310.pyc <br>
    │   ├── StoreInfoManager.cpython-310.pyc <br>
    │   ├── pharmacy_info.cpython-310.pyc <br>
    │   └── resources_rc.cpython-310.pyc <br>
    ├── pharmacy_info.py <br>
    └── resources_rc.py <br>

Total: 14 directories, 116 files
