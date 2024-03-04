import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DATABASE = "access_log_database"
DATABASE_USER = "postgres"
DATABASE_PASS = "insert_db_password"

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
    try:
        command = ("""
        CREATE TABLE logs (
            id SERIAL PRIMARY KEY,
            time_open TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            time_close TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(command)

        conn.commit()
        print("access_log table is created")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error when creating table", error)
    
    finally:
        if conn is not None:
            cur.close()
            conn.close()

opt = int(input("Menu: \n1.Create DB \n2.Create Table\n>"))
if opt == 1:
    create_database()
elif opt == 2:
    create_log_table()