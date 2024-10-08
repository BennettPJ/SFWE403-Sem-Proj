#Dashboard.py
import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import resources_rc  # Import the compiled resource file
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QTime

class Dashboard(QMainWindow):
    def __init__(self, widget):  # Accept the widget as an argument
        super(Dashboard, self).__init__()
        self.widget = widget  # Store the QStackedWidget reference

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'UI', 'Dashboard.ui')
        loadUi(ui_path, self)

        # Ensure the logout button works
        self.logOut.clicked.connect(self.logOutUser)

        # Set QLCDNumber to handle 8 digits (HH:MM:SS)
        self.clock.setSegmentStyle(self.clock.Flat)  # Optional: for cleaner LCD look
        self.clock.setDigitCount(8)  # HH:MM:SS requires 8 characters

        # Set up the timer to update the clock every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  # Update every 1 second (1000 milliseconds)

        # Initial clock display
        self.update_clock()

    def update_clock(self):
        # Get the current time
        current_time = QTime.currentTime()

        # Format the time string as HH:MM:SS
        time_string = current_time.toString('hh:mm AP')

        # Display the time on the LCD in string mode
        self.clock.display(time_string)

    def logOutUser(self):
        from src.LogInGUI import MainUI

        # Check if the login screen is already in the stack
        for i in range(self.widget.count()):
            if isinstance(self.widget.widget(i), MainUI):
                self.widget.setCurrentIndex(self.widget.indexOf(self.widget.widget(i)))
                return

        # If not in the stack, create a new instance of MainUI and add it to the stack
        login_screen = MainUI(self.widget)
        self.widget.addWidget(login_screen)
        self.widget.setCurrentIndex(self.widget.indexOf(login_screen))
