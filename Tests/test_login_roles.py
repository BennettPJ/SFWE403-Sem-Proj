import sys
import os
import csv

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from LoginRoles import LoginRoles  # Adjust the import path after updating the sys.path

def setup_test_file(test_file):
    """Setup a fresh test file with the correct headers."""
    with open(test_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Email', 'Password', 'Role', 'Locked_counter', 'Locked_status'])

def run_tests():
    # Set up a test CSV file path (this will be created in the test directory)
    test_roles_file = os.path.join(os.path.dirname(__file__), 'Test_databases/test_db_user_account.csv')
    
    # Set up the test file with correct headers before testing
    setup_test_file(test_roles_file)
    
    # Instantiate the LoginRoles class using the test file
    login_roles = LoginRoles(roles_file=test_roles_file)
    
    # Test 1: Create accounts
    print("\nTest 1: Create Accounts")
    login_roles.create_account('pharmacist', 'john_doe', 'password123', 'john@example.com')
    login_roles.create_account('technician', 'jane_doe', 'securepass', 'jane@example.com')
    login_roles.create_account('manager', 'admin_user', 'adminpass', 'admin@example.com')
    
    # Test 2: Attempt to create a duplicate account
    print("\nTest 2: Attempt to Create Duplicate Account")
    login_roles.create_account('pharmacist', 'john_doe', 'anotherpassword', 'john@example.com')
    
    # Test 3: Log in with a valid account
    print("\nTest 3: Login with Valid Account")
    success, message = login_roles.login('john_doe', 'password123')
    print(message)
    
    # Test 4: Log in with an invalid password
    print("\nTest 4: Login with Invalid Password")
    success, message = login_roles.login('john_doe', 'wrongpassword')
    print(message)
    
    # Test 5: Log in with a locked account after multiple failures
    print("\nTest 5: Lock Account After Multiple Failed Attempts")
    for _ in range(6):
        success, message = login_roles.login('john_doe', 'wrongpassword')
        print(message)
    
    # Test 6: Log in with the admin account
    print("\nTest 6: Login with Admin Account")
    success, message = login_roles.login('admin', 'password')
    print(message)
    
    # Test 7: Find user role
    print("\nTest 7: Find User Role")
    role = login_roles.find_user_role('jane_doe')
    print(f"Role for 'jane_doe': {role}")
    
    # Test 8: Update an account's email, password, and role
    print("\nTest 8: Update an Account")
    login_roles.update_account('john_doe', new_email='john_new@example.com', new_password='newpassword123', new_role='technician')
    success, message = login_roles.login('john_doe', 'newpassword123')
    print(message)
    updated_role = login_roles.find_user_role('john_doe')
    print(f"Updated role for 'john_doe': {updated_role}")
    
    # Test 9: Update an account that doesn't exist
    print("\nTest 9: Update Non-Existent Account")
    result = login_roles.update_account('non_existent_user', new_email='non_existent@example.com')
    print(f"Update non-existent user result: {result}")
    
    # Test 10: Remove an account
    print("\nTest 10: Remove an Account")
    login_roles.remove_account('jane_doe')
    
    # Test 11: Attempt to login with removed account
    print("\nTest 11: Login with Removed Account")
    success, message = login_roles.login('jane_doe', 'securepass')
    print(message)
    
    # Test 12: Attempt to remove a non-existent account
    print("\nTest 12: Remove Non-Existent Account")
    result = login_roles.remove_account('non_existent_user')
    print(f"Remove non-existent user result: {result}")
    
    # Test 13: Ensure 'Locked_counter' and 'Locked_status' reset after a successful login
    print("\nTest 13: Locked Counter Reset After Successful Login")
    login_roles.create_account('cashier', 'cashier_user', 'cashierpass', 'cashier@example.com')
    for _ in range(4):  # Four failed login attempts
        login_roles.login('cashier_user', 'wrongpassword')
    # Successful login should reset counter
    success, message = login_roles.login('cashier_user', 'cashierpass')
    print(message)
    # Verify locked status and counter reset
    user_data = login_roles.get_user_data('cashier_user')
    print(f"Locked Counter: {user_data['Locked_counter']}, Locked Status: {user_data['Locked_status']}")

    # Clean up the test file (optional)
    # os.remove(test_roles_file)

if __name__ == "__main__":
    run_tests()