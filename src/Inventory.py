class Inventory:
    def __init__(self, low_stock_threshold=10):
        #Initializes the inventory with an empty stock dictionary and a low stock threshold.
        #:param low_stock_threshold: The minimum stock level before a notification is triggered.
        
        self.stock = {}  # Holds {Medication: Quantity} pairs
        self.low_stock_threshold = low_stock_threshold


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