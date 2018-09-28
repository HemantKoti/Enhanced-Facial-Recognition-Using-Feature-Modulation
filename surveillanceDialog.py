# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 16:13:40 2018

@author: SachdeBS
"""

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from faceDetectionWidget import FaceDetectionWidget
from recordVideo import RecordVideo
from databaseManager import DatabaseManager

# This is the GUI created from QT designer
qtCreatorFile = "surveillance.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class SurveillanceDialog(QtWidgets.QDialog, Ui_MainWindow):
    
    """
    Declaring global variables
    """
    
    """
    Description:
      This function will initialise the gui and associate the function calls
      with various widgets
    """
    # handle the case when the change is at the last I think there is rounding of index somewhere
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.face_detection_widget = FaceDetectionWidget()      
        self.record_video = RecordVideo()
        
        # Connect the image data signal and slot together
        image_data_slot = self.face_detection_widget.facerec_from_webcam
        self.record_video.image_data.connect(image_data_slot)
        
        comboboxChanged = self.comboboxChangedEvent
        self.face_detection_widget.comboValueChanged.connect(comboboxChanged)
        
        self.record_video.start_recording()
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.face_detection_widget)
            
        self.widget.setLayout(layout)
        self.comboBox.currentTextChanged.connect(self.updateInfo)
        self.dbMgr = DatabaseManager()
    
    def comboboxChangedEvent(self, name):
        if name != "Unknown":
            self.comboBox.addItem(str(name))
        
    def updateInfo(self):
        fileName =  ""
        filePath = ""
        fileDescription = ""
        for result in self.dbMgr.identityCollection.find({"id": str(self.comboBox.currentText())}):
            filePath = result['FilePath']
            fileName = result['Name']
            fileDescription = result['Description']
            
        pixmapLeft = QPixmap(filePath)
        m_pixmapLeft = pixmapLeft.scaled(249,173, QtCore.Qt.IgnoreAspectRatio)
        self.currentImageLabel.setPixmap(m_pixmapLeft)
        self.textBrowser.setText("Name: " + fileName + "\n\nDescription: " + fileDescription)