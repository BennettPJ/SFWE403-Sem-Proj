import sys
import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLineEdit, QComboBox
from PyQt5.uic import loadUi
from src.Login_roles import LoginRoles
from src.Dashboard import Dashboard

class Patient():
    def __init__(self):
        #name
        #age
        pass

    def createPatient(self):
        pass
    
    def SetData(self):
        if "patient" in self.roles:
            name = input("Enter Patient Name: ")
            age = input("Enter Patient Age: ")
        else:
            print("Cannot update non-patient data")
