import json
import cj_loader as customerFactor
import cj_interpreter as inter
import db_generator as database
import resources as r

import sqlite3

def assessCommericalJobs(startDate, endDate):
    exportedFileName = "CF_exported.csv"
    data = customerFactor.readOnly(exportedFileName)
    
    # Create SQLite database/tables
    # db.create(data)

    db = openConnections()

    

    closeConnections(db)
    
    # SQL Queries
    # 1. Filter by date range
    # 2. filter by employee
    # 3. filter by frequency
    # 4. search by name

def openConnections():
    db = {}

    customerConnection = sqlite3.connect(database.CustomerDb)
    jobConnection = sqlite3.connect(database.JobsDb)

    db.connections = {
        "customers": customerConnection,
        "jobs": jobConnection
    }

    db.customers = customerConnection.cursor()
    db.jobs = jobConnection.cursor()

    return db


def closeConnections(db):
    for key in db.connections:
        db.connections[key].close()

assessCommericalJobs("01/01/19", "11/13/22")