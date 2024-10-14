from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import os
import sys
from PyQt5.QtCore import pyqtSlot


class Purchases(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(Purchases, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Purchase.ui')
        loadUi(ui_path, self)

        self.grandTotalLabel.setText("Grand Total: $0.00")

        self.addItemButton.clicked.connect(self.add_item)
        self.removeItemButton.clicked.connect(self.remove_item)
        self.cancelButton.clicked.connect(self.cancelPurchase)
        self.Complete.clicked.connect(self.complete_purchase)

        # Connect changes in the ItemsTable to the function that recalculates the total.
        self.ItemsTable.itemChanged.connect(self.update_grand_total)

    def cancelPurchase(self):
        from src.Dashboard import Dashboard  # Importing MainUI inside the function to avoid circular import

        # Always create a new instance of MainUI
        dashboard = Dashboard(self.widget)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))

    @pyqtSlot()
    def complete_purchase(self):
        grand_total = self.grandTotalLabel.text()

        # Show a confirmation message box
        msg = QMessageBox()
        msg.setWindowTitle("Purchase Complete")
        msg.setText(f"Purchase completed successfully.\n{grand_total}")
        msg.setStandardButtons(QMessageBox.Ok)

        # Connect the button click to return to the dashboard
        if msg.exec_() == QMessageBox.Ok:
            self.reset_table()  # Reset the table before returning
            self.returnToDashboard()

    def reset_table(self):
        """Clear all items from the ItemsTable while keeping the rows."""
        for row in range(self.ItemsTable.rowCount()):
            for column in range(self.ItemsTable.columnCount()):
                self.ItemsTable.setItem(row, column, QTableWidgetItem(""))  # Clear the cell contents

        self.grandTotalLabel.setText("Grand Total: $0.00")  # Reset the grand total label


    def returnToDashboard(self):
        from src.Dashboard import Dashboard

        # Check if the dashboard is already in the stacked widget
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), Dashboard):
                self.widget.setCurrentIndex(i)  # Switch to existing Dashboard
                return
        
        # If not found, create the dashboard and add it to the stacked widget
        dashboard = Dashboard(self.widget)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))

    def update_grand_total(self, item=None):
        grand_total = 0.0

        # Temporarily disconnect the signal to avoid recursion.
        self.ItemsTable.blockSignals(True)

        try:
            # Iterate through each row to calculate the total cost of each item.
            for row in range(self.ItemsTable.rowCount()):
                quantity_item = self.ItemsTable.item(row, 1)  # Assuming 2nd column is Quantity
                price_item = self.ItemsTable.item(row, 2)     # Assuming 3rd column is Price

                try:
                    quantity = int(quantity_item.text()) if quantity_item else 0
                    price = float(price_item.text()) if price_item else 0.0
                except ValueError:
                    quantity = 0
                    price = 0.0

                # Calculate total cost for each row.
                total_cost = quantity * price

                # Update the total cost in the 4th column (index 3).
                self.ItemsTable.setItem(row, 3, QTableWidgetItem(f"{total_cost:.2f}"))

                # Add to grand total.
                grand_total += total_cost

            # Update the grand total label.
            self.grandTotalLabel.setText(f"Grand Total: ${grand_total:.2f}")
        finally:
            # Reconnect the signal after updating.
            self.ItemsTable.blockSignals(False)

    def add_item(self):
        row_count = self.ItemsTable.rowCount()
        self.ItemsTable.insertRow(row_count)

    def remove_item(self):
        selected_items = self.ItemsTable.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            self.ItemsTable.removeRow(selected_row)
            self.update_grand_total()
        else:
            QMessageBox.warning(self, "Warning", "Please select a row to remove.")
