"""Command-Line Interface to upload data from files to database"""

import os
import argparse
import psycopg2

# pylint: disable=line-too-long

def connect_db(dbname, host, port, username):
    """Connects to database"""
    db_password = input("Enter DB password: ")
    conn = psycopg2.connect(
        database=dbname, user=username, password=db_password, host=host, port=port
    )
    return conn


def query_taxis(taxi_id, plate):
    """Query to insert data into taxis table"""
    return f"INSERT INTO taxis (id, plate) VALUES ({taxi_id},'{plate}');"


def query_trajectories(taxi_id, date, latitude, longitude):
    """Query to insert data into trajectories table"""
    return f"INSERT INTO trajectories (taxi_id, date, latitude, longitude) VALUES ({taxi_id}, '{date}',{latitude},{longitude});"


def get_queries(file_type, file):
    """Creates a query for each line of the file and returns a list with queries"""
    queries = []
    for line in file:
        values = line.strip().split(",") # turns "7249,CNCJ-2997" into ["7249", "CNCJ-2997"]
        if file_type == "taxis":
            query = query_taxis(*values)
        if file_type == "trajectories":
            query = query_trajectories(*values)
        queries.append(query)
    return queries


def insert_data(path, file_type, dbname, host, port, username):
    """Connects to database, reads the files and inserts data into the table"""
    conn = connect_db(dbname, host, port, username)
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                file_name = entry.name
                file_path = f"{path}/{file_name}"
                with open(file_path, "r", encoding="utf-8") as file:
                    queries = get_queries(file_type, file)
                    # if queries is not empty, the data is inserted
                    if queries:
                        cur = conn.cursor()
                        cur.execute(" ".join(queries))
                        conn.commit()
                        print(f"Done with file {file_name}")
    conn.close()


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
