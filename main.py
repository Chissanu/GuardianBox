import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

DATABASE = "access_log_database"
DATABASE_USER = "postgres"
DATABASE_PASS = "Chissanu1"

def get_db_connection():
    conn = psycopg2.connect(
        dbname = DATABASE,
        user = DATABASE_USER,
        password = DATABASE_PASS,
        host = "localhost",
        port = "5432"
    )
    return conn

def create_database():
    try:
        conn = psycopg2.connect(f"user={DATABASE_USER} password={DATABASE_PASS}")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute(f"CREATE DATABASE {DATABASE}")

        print("Database created successfully")

    # Create database if not exists
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error when creating database", error)

    finally:
        if conn is not None:
            cur.close()
            conn.close()

def create_log_table():
    command = ("""
        CREATE TABLE logs (
            id SERIAL PRIMARY KEY,
            weight FLOAT DEFAULT 0.0,
            time_open TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            time_close TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    insert_to_database(command)

def insert_to_database(command):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(command)
        conn.commit()
        print("Success")
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error executing SQL command \n" + command)
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def openCrate():
    timestamp_val = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Open crate sum
    crateOpen = "t"
    while crateOpen == "t":
        crateOpen = input("Still open? t/f >")
    timeclose_val = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    weight = getWeight()

    command = f"INSERT INTO logs (weight,time_open, time_close) values ('{weight}','{timestamp_val}','{timeclose_val}')"
    insert_to_database(command)

def getWeight():
    # Psudo weight
    return 5.1


opt = None
while opt != 0:
    if opt == 1:
        create_database()
    elif opt == 2:
        create_log_table()
    elif opt == 3:
        openCrate()
    opt = int(input("Menu: \n0.Exit\n1.Create DB \n2.Create Table\n3.Open Crate \n>"))