# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 14:12:03 2018

@author: SachdeBS
"""

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPalette, QBrush
from databaseManager import DatabaseManager

import sys
import identifyDialog
import surveillanceDialog

# This is the GUI created from QT designer
qtCreatorFile = "mainGUI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    """
    Description:
      This function will initialise the gui and associate the function calls
      with various widgets
    """
              
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        # setting up the background
        oImage = QImage("backgroundMain5.png")
        sImage = oImage.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio)
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        
        # Connectivity with the dialog boxes
        self.surveillanceButton.clicked.connect(self.openSurveillanceDialog)
        self.identifyButton.clicked.connect(self.openIdentifyDialog)
        self.dbMgr = DatabaseManager()
                
    def openSurveillanceDialog(self):
        surveillance = surveillanceDialog.SurveillanceDialog()
        surveillance.exec()
        
    def openIdentifyDialog(self):
        identify = identifyDialog.IdentifyDialog()
        identify.exec()
                
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())