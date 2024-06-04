"""Command-Line Interface to upload data from files to database"""

import os
import argparse
import psycopg2


def query_taxis(taxi_id, plate):
    """Query to insert data into taxis table"""
    return f"INSERT INTO taxis (id, plate) VALUES ({taxi_id},'{plate}');"


def query_trajectories(taxi_id, date, latitude, longitude):
    """Query to insert data into trajectories table"""
    return f"INSERT INTO trajectories (taxi_id, date, latitude, longitude) VALUES ({taxi_id}, '{date}',{latitude},{longitude});"


def insert_data(path, file_type, dbname, host, port, username):
    """Connects to database, reads the files and inserts data into the table"""
    db_password = input("Enter DB password: ")
    conn = psycopg2.connect(
        database=dbname, user=username, password=db_password, host=host, port=port
    )
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                file_name = entry.name
                file_path = f"{path}/{file_name}"
                # opens every file in directory
                with open(file_path, "r", encoding="utf-8") as file:
                    queries = []
                    # reads every line of the file and creates a query for each one
                    for line in file:
                        values = line.split(",") # turns "7249,CNCJ-2997" into ["7249", "CNCJ-2997"]
                        if file_type == "taxis":
                            query = query_taxis(*values)
                        if file_type == "trajectories":
                            query = query_trajectories(*values)
                        queries.append(query)
                    # only executes if queries is not empty
                    if queries:
                        # inserts data after reading the file
                        cur = conn.cursor()
                        cur.execute(" ".join(queries))
                        conn.commit()
                        print(f"Done with file {file_name}")
    conn.close() # closes the connection to the database


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Directory with files")
    parser.add_argument("--type", choices=["taxis", "trajectories"], help="Type of file")
    parser.add_argument("--dbname", help="Database name")
    parser.add_argument("--host", help="Database host")
    parser.add_argument("--port", help="Database port")
    parser.add_argument("--username", help="Database username")
    args = parser.parse_args()
    insert_data(args.path, args.type, args.dbname, args.host, args.port, args.username)
