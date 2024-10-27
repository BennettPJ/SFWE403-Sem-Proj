import sys
import os

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from Inventory import Inventory  # Adjust import path as needed

def run_tests():
    # Create an instance of the Inventory class
    inv_file = os.path.join(os.path.dirname(__file__), 'Test_databases/test_db_inventory.csv')
    filled_file = os.path.join(os.path.dirname(__file__), 'Test_databases/test_db_filled_Prescriptions.csv')
    picked_file = os.path.join(os.path.dirname(__file__), 'Test_databases/test_db_picked_up_prescriptions.csv')

    inventory = Inventory(
        inventory_file=inv_file,
        filled_file=filled_file,
        picked_up_file=picked_file
    )
    
    # Test 1: View the current stock
    print("\nTest 1: View Current Stock")
    inventory.view_stock()

    # Test 2: Update stock - existing medication
    print("\nTest 2: Update Stock (Existing Medication)")
    inventory.update_stock('Aspirin', 10)  # Assuming 'Aspirin' is in the CSV
    inventory.view_stock()

    # Test 3: Update stock - new medication
    print("\nTest 3: Update Stock (New Medication)")
    inventory.update_stock('Ibuprofen', 50)  # Adding new medication
    inventory.view_stock()

    # Test 4: Remove medication
    print("\nTest 4: Remove Medication")
    inventory.remove_medication('Aspirin')  # Removing 'Aspirin'
    inventory.view_stock()

    # Test 5: Check low stock levels
    print("\nTest 5: Check Low Stock Levels")
    inventory.check_low_stock()  # Check for any medication below the threshold

    # Test 6: Fill a prescription
    print("\nTest 6: Fill Prescription")
    inventory.fill_prescription('Ibuprofen', 5)  # Fill prescription for 'Ibuprofen'
    inventory.view_stock()
    inventory.view_filled_prescriptions()

    # Test 7: Pick up a prescription
    print("\nTest 7: Pick Up Prescription")
    inventory.pick_up_prescription('Ibuprofen', 5)  # Pick up the 'Ibuprofen' prescription
    inventory.view_picked_up_prescriptions()

     # Test 8: Update stock - new medication
    print("\nTest 8: Update Stock (New Medication)")
    inventory.update_stock('test', 1)  # Adding new medication
    inventory.view_stock()
    
    # Test 9: Check low stock levels
    print("\nTest 9: Check Low Stock Levels")
    inventory.check_low_stock()  # Check for any medication below the threshold
    
    # Test 10: auto_order
    print("\nTest 10: Auto Order")
    inventory.auto_order()  # Auto order for 'test'
    inventory.view_stock()
    
    # Test 11: Fill a prescription
    print("\nTest 11: Fill Prescription")
    inventory.fill_prescription('test', 123)  # Fill prescription for 'Ibuprofen'
    inventory.view_stock()
    inventory.view_filled_prescriptions()
    
    #test 12: update stock
    print("\nTest 12: Update Stock")
    inventory.view_stock()
    inventory.update_stock('test', 35)  # Adding new medication
    
    # Test 13: fill a prescription
    print("\nTest 13: Fill Prescription")
    inventory.fill_prescription('test', 1)  # Fill prescription for 'Ibuprofen'
    inventory.view_stock()
    inventory.view_filled_prescriptions()
    
    # # Test 14: clear picked up prescriptions
    # print("\nTest 14: Clear Picked Up Prescriptions")
    # inventory.clear_picked_up_prescriptions()
    # inventory.view_picked_up_prescriptions()
    
if __name__ == "__main__":
    run_tests()