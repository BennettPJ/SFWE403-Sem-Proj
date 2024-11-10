#InventoryUI.py
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import os
from Inventory import Inventory
from LoginRoles import LoginRoles


class InventoryUI(QMainWindow):
    def __init__(self, widget, username):
        super(InventoryUI, self).__init__()
        self.widget = widget
        self.inventory = Inventory()
        self.username = username

        # Load the UI file
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Inventory.ui')
        if not os.path.exists(ui_path):
            print(f"UI file not found at: {ui_path}")
        loadUi(ui_path, self)

        # Connect buttons
        self.cancelButton.clicked.connect(self.cancel)
        self.viewStockButton.clicked.connect(self.load_inventory_into_table)
        self.updateStockButton.clicked.connect(self.update_inventory)
        self.autoOrderButton.clicked.connect(self.auto_order_stock)
        self.lowStockButton.clicked.connect(self.check_low_stock)
        self.exp_date.clicked.connect(self.check_exp_date)
        self.inv_row.clicked.connect(self.add_empty_row)

        self.setMinimumSize(1200, 600)
        self.initialize_table()
        self.setup_ui()

    def setup_ui(self):
        roles = LoginRoles()
        user_role = roles.find_user_role(self.username)

        if user_role != 'manager':
            self.autoOrderButton.setEnabled(False)
            self.exp_date.setEnabled(False)

    def initialize_table(self):
        self.ItemsTable.setColumnCount(8)
        self.ItemsTable.setHorizontalHeaderLabels(
            ['Medication', 'ID', 'Quantity', 'Price', 'Expiration Date', 'Date Added', 'Date Updated', 'Date Removed']
        )
        self.load_inventory_into_table()

    def load_inventory_into_table(self):
        self.ItemsTable.setRowCount(0)
        inventory_data = self.inventory.read_inventory_data()

        for i, item in enumerate(inventory_data):
            self.ItemsTable.insertRow(i)
            self.ItemsTable.setItem(i, 0, QTableWidgetItem(item['Medication']))
            self.ItemsTable.setItem(i, 1, QTableWidgetItem(item['ID']))
            self.ItemsTable.setItem(i, 2, QTableWidgetItem(item['Quantity']))
            self.ItemsTable.setItem(i, 3, QTableWidgetItem(item['Price']))
            self.ItemsTable.setItem(i, 4, QTableWidgetItem(item['Expiration Date']))
            self.ItemsTable.setItem(i, 5, QTableWidgetItem(item.get('Date Added', '')))
            self.ItemsTable.setItem(i, 6, QTableWidgetItem(item.get('Date Updated', '')))
            self.ItemsTable.setItem(i, 7, QTableWidgetItem(item.get('Date Removed', '')))

        self.add_empty_row()

    def add_empty_row(self):
        row_count = self.ItemsTable.rowCount()
        self.ItemsTable.insertRow(row_count)
        for col in range(8):
            self.ItemsTable.setItem(row_count, col, QTableWidgetItem(""))

    def update_inventory(self):
        selected_row = self.ItemsTable.currentRow()
        if selected_row != -1:
            medication = self.ItemsTable.item(selected_row, 0).text()
            item_id = self.ItemsTable.item(selected_row, 1).text()
            quantity = self.ItemsTable.item(selected_row, 2).text()
            price = self.ItemsTable.item(selected_row, 3).text()
            exp_date = self.ItemsTable.item(selected_row, 4).text()

            try:
                new_quantity = int(quantity)
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid quantity entered.")
                return

            self.inventory.update_stock(medication, item_id, new_quantity, exp_date, price)
            QMessageBox.information(
                self, "Success", f"Updated {medication} (ID: {item_id}) with new stock."
            )
            self.load_inventory_into_table()
        else:
            QMessageBox.warning(self, "Error", "Please select a row to update!")

    def auto_order_stock(self):
        reorder_made = self.inventory.auto_order()
        if reorder_made:
            QMessageBox.information(self, "Auto Order", "Auto reorder placed for low-stock items.")
        else:
            QMessageBox.information(self, "Auto Order", "No items required reordering.")
        self.load_inventory_into_table()

    def check_low_stock(self):
        low_stock_items = self.inventory.check_low_stock()
        if low_stock_items:
            message = "Low stock alert for the following medications:\n" + "\n".join(
                f"- {item[0]} (ID: {item[1]}): {item[2]} units left"
                for item in low_stock_items
            )
            QMessageBox.warning(self, "Low Stock Alert", message)
        else:
            QMessageBox.information(self, "Low Stock Alert", "No low-stock medications.")

    def check_exp_date(self):
        exp_date_items = self.inventory.check_exp_date()
        if exp_date_items:
            message = "Expiration date alert for the following medications:\n" + "\n".join(
                f"- {item[0]} (ID: {item[1]}): Expiration Date: {item[3]}"
                for item in exp_date_items
            )
            QMessageBox.warning(self, "Expiration Date Alert", message)
        else:
            QMessageBox.information(self, "Expiration Date Alert", "No medications near expiration.")

    def cancel(self):
        from src.Dashboard import Dashboard
        dashboard = Dashboard(self.widget, self.username)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))
        self.widget.setFixedSize(1050, 600)
