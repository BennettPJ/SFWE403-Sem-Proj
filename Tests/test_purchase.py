import sys
import os 
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from Purchases import Purchases # Adjust import path as needed

def setup_test_file(test_file):
    """Setup a fresh test file with the correct headers."""
    with open(test_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Item, Quantity, Price', 'Total'])
        
def run_tests():
    test_roles_file = os.path.join(os.path.dirname(__file__), 'Test_databases/test_db_purchase.csv')
    setup_test_file(test_roles_file)
    
    purchase = Purchases(purchase_file=test_roles_file)
    
    print("\nTest 1: Add Items")
    purchase.add_item('Apple', 1, 1)
    print("\nTest 2: Add Duplicate Items")
    purchase.add_item('Apple', 1,1)
    
    print("\nTest 3: Add Multiple Items")
    purchase.add_item('Orange', 2,2)
    purchase.add_item('Banana', 3,3)
    
    print("\nTest 4: Calculate Total")
    purchase.update_grand_total()
    
    print("\nTest 5: Remove Item")
    purchase.remove_item('Orange')
    
    print("\nTest 6: Calculate Total")
    purchase.update_grand_total()
    
    print("\nTest 7: Print Receipt")
    purchase.print_receipt()
    
    print("\nTest 8: Cancel Purchase")
    purchase.cancelPurchase()
    
    print("\nTest 9: Complete Purchase")
    purchase.complete_purchase()
    
if __name__ == "__main__":
    run_tests()
        