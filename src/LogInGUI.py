from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import os

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        # Load the UI file relative to the project's root
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ui', 'LogInGUI.ui')
        loadUi(ui_path, self)
