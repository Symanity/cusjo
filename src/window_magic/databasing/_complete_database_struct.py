import sqlite3
import os
import csv

from src.window_magic import _resources as r

DATABASE_FILE_NAME = 'window_magic_complete.db'
DATABASE_LOCATION = os.path.join(r.database_path, DATABASE_FILE_NAME)

CSV_FILENAME = "window_magic_complete_history.csv"
CSV_LOCATION = os.path.join(r.database_path, r.csv_folder_name,CSV_FILENAME)

JOB_HISTORY_TABLE = 'WINDOW_MAGIC_JOB_HISTORY'

def create(job_tubles):
    # Connect to the database
    conn = sqlite3.connect(DATABASE_LOCATION)
    cursor = conn.cursor()

    # Create the table
    cursor.execute("DROP TABLE IF EXISTS {}".format(JOB_HISTORY_TABLE))
    cursor.execute(
        '''CREATE TABLE {} (
            customer_id INTEGER, 
            customer_name TEXT, 
            customer_address TEXT, 
            services TEXT,
            job_date TEXT, 
            price REAL,
            duration REAL, 
            employee TEXT)'''.format(JOB_HISTORY_TABLE))

    # Iterate through the list of tuples and insert the values into the table
    for job in job_tubles:
        cursor.execute("""INSERT INTO {} (
            customer_id, 
            customer_name, 
            customer_address, 
            services, 
            job_date, 
            price,
            duration, 
            employee) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""".format(JOB_HISTORY_TABLE), job)

    # Save the changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()
    print('[STATUS] Built {} table'.format(JOB_HISTORY_TABLE))


def writeCSV():
    # Connect to the database file
    conn = sqlite3.connect(DATABASE_LOCATION)

    # Create a cursor object
    cursor = conn.cursor()

    # Select all rows from the CUSTOMERS table
    cursor.execute("SELECT * FROM {}".format(JOB_HISTORY_TABLE))

    # Fetch all rows from the CUSTOMERS table
    customers = cursor.fetchall()

    # Write the rows to a CSV file
    with open(CSV_LOCATION, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(customers)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    print('[BUILD] csv file created: {}'.format(CSV_LOCATION))

# args must be of type Tuble
def ask(sqlite_query, args=None):
    response = []
    conn = sqlite3.connect(DATABASE_LOCATION)
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