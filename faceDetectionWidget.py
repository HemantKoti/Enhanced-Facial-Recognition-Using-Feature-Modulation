# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 18:55:20 2018

@author: HemantKo
"""

import cv2
import numpy as np
import face_recognition

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from databaseManager import DatabaseManager

class FaceDetectionWidget(QtWidgets.QWidget):
    
    comboValueChanged = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)
        self.process_this_frame = True
        self._comboboxNames = []
        self.dbMgr = DatabaseManager()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    @property
    def comboboxNames(self):
        return self._comboboxNames

    @comboboxNames.setter
    def comboboxNames(self, value):
        if value not in self.comboboxNames:
            print(str(value))
            self._comboboxNames.append(value)
            self.comboValueChanged.emit(value)

    def facerec_from_webcam(self, frame):
        
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        known_face_encodings = []
        known_face_names = []
        
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]   
        
        faces = self.dbMgr.identityCollection.find({})
        for result in faces:
            known_face_encodings.append(result['Encodings'])
            known_face_names.append(result['id'])
        
        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.6)
                name = "Unknown"
    
                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                self.comboboxNames = name
                face_names.append(name)
    
        self.process_this_frame = not self.process_this_frame
    
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
    
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        self.image = self.get_qimage(frame)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()
        