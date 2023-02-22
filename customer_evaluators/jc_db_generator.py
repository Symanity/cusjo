# Job consideration database

import sqlite3
import os
import csv
import resources as r

JC_DB_NAME = 'jc_history.db'
JC_DB = os.path.join(r.database_path, JC_DB_NAME)

tbl_consideredJobs = 'CONSIDERED_JOBS'

def create(serviceObjs):
    # Connect to the database
    conn = sqlite3.connect(JC_DB)
    cursor = conn.cursor()

    # Create the table
    cursor.execute("DROP TABLE IF EXISTS {}".format(tbl_consideredJobs))
    cursor.execute(
        '''CREATE TABLE {} (
            customer_id INTEGER, 
            customer_name TEXT, 
            customer_address TEXT, 
            services TEXT,
            job_date TEXT, 
            price REAL,
            duration REAL, 
            employee TEXT)'''.format(tbl_consideredJobs))

    # Iterate through the list of tuples and insert the values into the table
    for t in serviceObjs:
        cursor.execute("""INSERT INTO {} (
            customer_id, 
            customer_name, 
            customer_address, 
            services, 
            job_date, 
            price,
            duration, 
            employee) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""".format(tbl_consideredJobs), t)

    # Save the changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()
    print('[STATUS] Built {} table'.format(tbl_consideredJobs))


def writeCSV():
    csv_foldername = "csv_considered_history"
    csv_considered_jobs = os.path.join(r.database_path, csv_foldername,"considered_history.csv")

    # Connect to the database file
    conn = sqlite3.connect(JC_DB)

    # Create a cursor object
    cursor = conn.cursor()

    # Select all rows from the CUSTOMERS table
    cursor.execute("SELECT * FROM {}".format(tbl_consideredJobs))

    # Fetch all rows from the CUSTOMERS table
    customers = cursor.fetchall()

    # Write the rows to a CSV file
    with open(csv_considered_jobs, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(customers)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    print('[BUILD] csv file created: {}'.format(csv_considered_jobs))

    # args must be of type Tuble
def ask(sqlite_query, args=None):
    response = []
    conn = sqlite3.connect(JC_DB)
    cursor = conn.cursor()

    if args:
        # Execute the query with the parameter
        cursor.execute(sqlite_query, args)
    else:
        # Execute the SQL command
        cursor.execute(sqlite_query)

    # Fetch the results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        response.append(row)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return response