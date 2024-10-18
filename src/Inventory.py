from LoginRoles import LoginRoles  # Import the LoginRoles class
class Inventory:
    def __init__(self, low_stock_threshold=10):
        #Initializes the inventory with an empty stock dictionary and a low stock threshold.
        #:param low_stock_threshold: The minimum stock level before a notification is triggered.
        
        self.stock = {}  # Holds {Medication: Quantity} pairs
        self.low_stock_threshold = low_stock_threshold
        self.filled_prescriptions = [] #list to track filled prescriptions
        self.picked_up_prescriptions = [] #list to track picked up prescriptions
        self.login_roles = LoginRoles()  # Create an instance of the LoginRoles class


    def view_stock(self):
        #Displays all medications and their quantities in the inventory.
        if not self.stock:
            print("The inventory is currently empty.")
        else:
            print("Current inventory stock:")
            for medication, quantity in self.stock.items():
                print(f"{medication}: {quantity} units")


    def update_stock(self, medication, quantity):
        #Updates the stock for a given medication. If the medication is not in the inventory, it adds it. If the medication already exists, it increments the current quantity.
        #:param medication: The name of the medication to add/update.
        #:param quantity: The amount to add to the current stock.

        if medication in self.stock:
            self.stock[medication] += quantity
        else:
            self.stock[medication] = quantity
        print(f"Updated stock for {medication}: {self.stock[medication]} units now available.")
        

    def remove_medication(self, medication):
        #Removes a medication from the inventory.
        #:param medication: The name of the medication to remove.
        
        if medication in self.stock:
            del self.stock[medication]
            print(f"{medication} has been removed from the inventory.")
        else:
            print(f"{medication} is not in the inventory.")


    def check_low_stock(self):
        #Checks for medications that are below the low stock threshold and prints a notification.
        low_stock_items = [medication for medication, quantity in self.stock.items() if quantity < self.low_stock_threshold]
        if low_stock_items:
            print("Low stock alert for the following medications:")
            for item in low_stock_items:
                print(f"{item}: Only {self.stock[item]} units left!")
        else:
            print("No low stock medications at the moment.")
            
            
    def auto_order(self, medication):
        if self.stock[medication] < self.auto_reorder_threshold:
            order_quantity = self.low_stock_threshold #order when stock is at the low threshold
            self.update_stock(medication, order_quantity)
            print(f"Automatic reorder placed for {medication}. {order_quantity} units added to stock.")


    def order_medication(self, medication, quantity, username, password):
        # Restricts ordering medications to managers only
        login_success, message = self.login_roles.login(username, password)
        
        if login_success:
            role = self.login_roles.find_user_role(username)
            if role == "manager":
                print(f"{username} (Manager) is ordering {quantity} units of {medication}.")
                self.update_stock(medication, quantity)
            else:
                print(f"Permission denied. Only managers can order medications.")
        else:
            print(f"Login failed: {message}")

            
    def fill_prescription(self, medication, quantity):
        #Fills a prescription by dispensing the requested quantity of a medication.
        if medication not in self.stock:
            print(f"{medication} is not in the inventory.")
            return
        
        if self.stock[medication] >= quantity:
            self.stock[medication] -= quantity
            self.fill_prescription.append((medication, quantity))
            print(f"{quantity} units of {medication} dispensed.")
        else:
            print(f"Insufficient stock for {medication}.")
        
        self.check_low_stock() #check if there is any low stock items now
        
        
    def add_new_prescription(self, medication, quantity):
        #Adds a new prescription to the inventory.
        self.update_stock(medication, quantity)
        print(f"New prescription added: {medication} - {quantity} units.")
        
        
    def pick_up_prescription(self, medication, quantity):
        #Tracks the pickup of a prescription by removing it from the filled prescriptions list.
        if (medication, quantity) in self.filled_prescriptions:
            self.filled_prescriptions.remove((medication, quantity))
            self.picked_up_prescriptions.append((medication, quantity))
            print(f"{quantity} units of {medication} picked up.")
        else:
            print("Prescription not found in filled prescriptions.")
            
            
    def view_filled_prescriptions(self):
        #Displays all filled prescriptions.
        if not self.filled_prescriptions:
            print("No filled prescriptions at the moment.")
        else:
            print("Filled prescriptions:")
            for medication, quantity in self.filled_prescriptions:
                print(f"{quantity} units of {medication}")
            
                
    def view_picked_up_prescriptions(self):
        #Displays all picked up prescriptions.
        if not self.picked_up_prescriptions:
            print("No picked up prescriptions at the moment.")
        else:
            print("Picked up prescriptions:")
            for prescription in self.picked_up_prescriptions:
                print(f"{prescription[1]} units of {prescription[0]}")
                