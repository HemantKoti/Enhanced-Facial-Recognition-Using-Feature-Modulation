# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 19:34:44 2018

@author: SachdeBS
"""
import pymongo

class DatabaseManager:    
    
    def __init__(self):
        self.CONN_STR = "mongodb://localhost:27017/"
        self.DATABASE_NAME = "FaceRecognition"
        self.IDENTITY_COLLECTION_NAME = "Identity"
        self.SURVEILLANCE_COLLECTION_NAME = "Surveillance"
        self.myclient = pymongo.MongoClient(str(self.CONN_STR))
        self.mydb = self.myclient[str(self.DATABASE_NAME)]
        self.identityCollection = self.mydb[str(self.IDENTITY_COLLECTION_NAME)]
        self.surveillanceCollection = self.mydb[str(self.SURVEILLANCE_COLLECTION_NAME)]
        