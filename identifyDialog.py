# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 17:24:14 2018

@author: SachdeBS
"""

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from databaseManager import DatabaseManager

import face_recognition

# This is the GUI created from QT designer
qtCreatorFile = "identifyGUI.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class IdentifyDialog(QtWidgets.QDialog, Ui_MainWindow):
    
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
        
        pixmapLeft = QPixmap('compareGirlLeft.jpg')
        m_pixmapLeft = pixmapLeft.scaled(249,370, QtCore.Qt.IgnoreAspectRatio)
        self.searchImageLabel.setPixmap(m_pixmapLeft)
        
        pixmapRight = QPixmap('compareGirlRight.jpg')
        m_pixmapRight = pixmapRight.scaled(249,370, QtCore.Qt.IgnoreAspectRatio)
        self.currentImageLabel.setPixmap(m_pixmapRight)
        
        self.browseButton.clicked.connect(self.importImage)
        self.searchButton.clicked.connect(self.searchImage)    
        self.dbMgr = DatabaseManager()
        self.file_name_list = []
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_description = []
        for result in self.dbMgr.identityCollection.find({}):
            self.known_face_encodings.append(result['Encodings'])
            self.known_face_names.append(result['Name'])
            self.file_name_list.append(result['FilePath'])
            self.known_face_description.append(result['Description'])
        
    def importImage(self):
        Options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", options=Options)
        self.imageLocation.setText(filename)
                
        pixmap = QPixmap(filename)
        m_pixmap = pixmap.scaled(249,370, QtCore.Qt.IgnoreAspectRatio)
        self.searchImageLabel.setPixmap(m_pixmap)
        
    def searchImage(self):
        
        unknown_image = face_recognition.load_image_file(self.imageLocation.text())
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        
        isResultFound = False
        for i in range(0,len(self.known_face_encodings)):           
            encapsulating_list = []           
            encapsulating_list.append(self.known_face_encodings[i])
            
            #compare the face encoding
            result = face_recognition.compare_faces(encapsulating_list,unknown_face_encoding, 0.7)
            
            #load the image
            pixmapRight = QPixmap(self.file_name_list[i])
            m_pixmapRight = pixmapRight.scaled(249,370, QtCore.Qt.IgnoreAspectRatio)
            self.currentImageLabel.setPixmap(m_pixmapRight)
            
            if result[0]:
                resultText = "Found Match\n\n" + "Name : " + self.known_face_names[i] + "\n\nDescription: " + self.known_face_description[i]              
                self.textBrowser.setText(resultText)
                isResultFound = True
                break
        
        if not isResultFound:
            resultText = "Match not found\n"
            self.textBrowser.setText(resultText)
            pixmapRight = QPixmap("")
            m_pixmapRight = pixmapRight.scaled(249,370, QtCore.Qt.IgnoreAspectRatio)
            self.currentImageLabel.setPixmap(m_pixmapRight)
        