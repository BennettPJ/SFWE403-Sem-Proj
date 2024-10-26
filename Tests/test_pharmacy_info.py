import sys
import os   
import csv

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from pharmacy_info import Pharmacy, PharmacySystem  # Adjust import path as needed

def setup_test_file(test_file):
    """Setup a fresh test file with the correct headers."""
    with open(test_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'website', 'address', 'owner', 'phone_number', 'hours'])
        

def run_tests():
    # Set up a test CSV file path (this will be created in the test directory)
    test_pharmacy_file = os.path.join(os.path.dirname(__file__), 'Test_databases/test_db_pharmacy.csv')
    
    # Set up the test file with correct headers before testing
    setup_test_file(test_pharmacy_file)
    
    # Instantiate the PharmacySystem class using the test file
    pharmacy_system = PharmacySystem(csv_file=test_pharmacy_file)
    
    # Test 1: Add pharmacy
    print("\nTest 1: Add Pharmacy")
    pharmacy = Pharmacy(
        name="Pharmacy A",
        website="www.pharmacyA.com",
        address="123 Main St, City, Country",
        owner="Owner A",
        phone_number="123-456-7890",
        hours="Mon-Fri: 9am-5pm"
    )
    pharmacy_system.add_pharmacy(pharmacy)
    pharmacy_system.save_to_csv()
    
    # Test 2: Load pharmacy from CSV
    print("\nTest 2: Load Pharmacy from CSV")
    pharmacy_system.load_from_csv()
    for pharmacy in pharmacy_system.pharmacies:
        print(pharmacy.to_dict())
        
if __name__ == "__main__":
    run_tests()