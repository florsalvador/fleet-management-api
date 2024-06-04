"""Main"""

# import cmd
import os
import argparse
import psycopg2


def query_taxis(taxi_id, plate):
    """Query to insert data into taxis table"""
    return f"INSERT INTO taxis_cli (id, plate) VALUES ({taxi_id},'{plate}');"


def query_trajectories(taxi_id, date, latitude, longitude):
    """Query to insert data into trajectories table"""
    return f"INSERT INTO trajectories_cli (taxi_id, date, latitude, longitude) VALUES ({taxi_id}, '{date}',{latitude},{longitude});"


def insert_data(path, file_type, dbname, host, port, username):
    """Connects to database, reads the files and inserts data into the table"""
    db_password = input("Enter DB password: ")
    conn = psycopg2.connect(
        database=dbname, user=username, password=db_password, host=host, port=port
    )
    with os.scandir(path) as entries:
        # num_files = len(list(entries))
        for entry in entries:
            if entry.is_file():
                file_name = entry.name
                # opens every file in directory
                file_path = f"{path}/{file_name}"
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
                    # inserts data after reading the file
                    cur = conn.cursor()
                    cur.execute(" ".join(queries))
                    conn.commit()
                    # print(f"Done with one file! (total: {num_files} files)")

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


#######################################


# def insert_into_taxis(taxi_id, plate):
#     """..."""
#     cur = conn.cursor()
#     cur.execute(
#         f"""INSERT INTO taxis (id, plate) VALUES ({taxi_id},{plate})"""
#     )
#     conn.commit()
#     conn.close()


# def insert_into_trajectories(taxi_id, date, latitude, longitude):
#     """..."""
#     cur = conn.cursor()
#     cur.execute(
#         f"""INSERT INTO trajectories (taxi_id, date, latitude, longitude) VALUES ({taxi_id}, {date},{latitude},{longitude})"""
#     )
#     conn.commit()
#     conn.close()


# # returns a Python list containing the names of the files and subdirectories in the directory
# entries = os.listdir('my_directory/')
# for entry in entries:
#     print(entry)

# # the same as before, other way to do it
# with os.scandir('my_directory/') as entries:
#     for entry in entries:
#         print(entry.name)

# # dog_breeds.txt example ("\r\n" indicates new line on windows):

# # Pug\r\n
# # Jack Russell Terrier\r\n
# # English Springer Spaniel\r\n
# # German Shepherd\r\n

# # opens file and closes it after done with it (not good to leave files opened)
# file = open('dog_breeds.txt', 'r', encoding="utf-8")
# try:
#     file.write("Hello, World!")
# finally:
#     file.close()

# # better to use this to close the file after done with it
# with open('dog_breeds.txt', 'r', encoding="utf-8") as file:
#     # for line in file.readlines(): # readlines() returns a list where each element in the list represents a line in the file:
#     for line in file: # the same as before but better
#         print(line, end='') # The end='' is to prevent Python from adding an additional newline to the text
#         # Pug
#         # Jack Russell Terrier
#         # English Springer Spaniel
#         # German Shepherd


# Inserting data into the table

# cur = conn.cursor()
# cur.execute("""
#     INSERT INTO Employee (ID,NAME,EMAIL) VALUES
#     (1,'Alan Walker','awalker@gmail.com'),
#     (2,'Steve Jobs','sjobs@gmail.com')
#   """)
# conn.commit()
# conn.close()

# Fetching the data from the database and displaying it into the terminal

# cur.execute("SELECT * FROM Employee")
# rows = cur.fetchall()
# for data in rows:
#     print("ID :" + str(data[0]))
#     print("NAME :" + data[1])
#     print("EMAIL :" + data[2])

# print('Data fetched successfully')
# conn.close()

# # Updating the data in the database

# cur = conn.cursor()
# cur.execute("UPDATE Employee set EMAI = 'updated@gmail.com' WHERE ID =1 ")
# conn.commit()
# print("Data updated Successfully")
# print("Total row affected "+str(cur.rowcount))
# conn.close()

# # Deleting data from the database

# cur = conn.cursor()
# cur.execute("DELETE FROM Employee WHERE ID =1 ")
# conn.commit()
# print("Data deleted Successfully")
# print("Total row affected "+str(cur.rowcount))
# conn.close()
