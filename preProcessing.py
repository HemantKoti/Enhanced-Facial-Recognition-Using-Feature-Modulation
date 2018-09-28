# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 15:06:43 2018

@author: SachdeBS
"""
import face_recognition
import os

from databaseManager import DatabaseManager

def saveEncodingInFile():
    dbMgr = DatabaseManager()
    folderName = "Images"
    faces = {}
    file_name_list = []
    for fileName in os.listdir(folderName):
        image = face_recognition.load_image_file(os.path.join(folderName, fileName))
        image_face_encoding = face_recognition.face_encodings(image)[0]
        faces[os.path.splitext(fileName)[0]] = image_face_encoding.tolist()
        file_name_list.append(os.path.join(folderName, fileName)) 
    
    for key, file_name in zip(faces.keys(), file_name_list):
        myvalue = { "id": key, "Name": "", "Encodings": faces[key] ,"Description": "", "Miscellaneous": "", "FilePath": file_name }
        result = list(dbMgr.identityCollection.find(myvalue))
        if len(result) == 0:
            dbMgr.identityCollection.insert_one(myvalue)

saveEncodingInFile()