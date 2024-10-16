from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.uic import loadUi
import os
import sys
from PyQt5.QtCore import pyqtSlot

class OrderMedication(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(OrderMedication, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'OrderMedication.ui')
        loadUi(ui_path, self)
                # Set a minimum size for the dashboard
        self.setMinimumSize(900, 600)  # Example size, you can adjust these values
        self.cancelButton.clicked.connect(self.cancelMedicationButton)
        self.addItemButton.clicked.connect(self.add_item)
        self.removeItemButton.clicked.connect(self.remove_item)


    def cancelMedicationButton(self):
        from src.Dashboard import Dashboard  # Importing MainUI inside the function to avoid circular import

        # Reset the table before returning to the dashboard.
        self.reset_table()

        # Always create a new instance of MainUI
        dashboard = Dashboard(self.widget)
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.indexOf(dashboard))

    def add_item(self):
        row_count = self.ItemsTable.rowCount()
        self.ItemsTable.insertRow(row_count)

    def remove_item(self):
        selected_items = self.ItemsTable.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            self.ItemsTable.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "Warning", "Please select a row to remove.")

    def reset_table(self):
        """Clear all items from the ItemsTable while keeping the rows."""
        for row in range(self.ItemsTable.rowCount()):
            for column in range(self.ItemsTable.columnCount()):
                self.ItemsTable.setItem(row, column, QTableWidgetItem(""))  # Clear the cell contents