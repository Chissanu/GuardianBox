import psycopg2
import time
import json
import threading
import paho.mqtt.client as mqtt
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime
from Controller import Contoller


DATABASE = "access_log_database"
DEFAULT_DB = "postgres"
DATABASE_USER = "pi"
DATABASE_PASS = "Chissanu1"
BROKER = "broker.hivemq.com"
PORT = 1883

chamber1_state = "Vacant"
chamber2_state = "Vacant"

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
        conn = psycopg2.connect(f"user={DATABASE_USER} password={DATABASE_PASS} dbname={DEFAULT_DB}")
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
            chamber_id VARCHAR,
            time_open TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            time_close TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    insert_to_database(command,"CREATE")

def insert_to_database(command,operation):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(command)
        conn.commit()

        if operation == "QUERY":
            rows = cur.fetchall()
            return rows
        print("Success")
        
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error executing SQL command \n" + command)
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def openCrate(chamber_id,timestamp_val,timeclose_val):
    command = f"INSERT INTO logs (chamber_id,time_open, time_close) values ('{chamber_id}', '{timestamp_val}','{timeclose_val}')"
    insert_to_database(command,"INSERT")
    get_logs()

def check_chamber1():
    global chamber1_state
    
    previous_message = None
    while True:
        distance = controller1.read_ultrasonic()
        if distance <= 26:
            print(f"Chamber 1 : Occupied with {distance}")
            chamber1_state = "Occupied"

        else:
            print(f"Chamber 1 : Vacant with {distance}")
            chamber1_state = "Vacant"

        if previous_message != chamber1_state:
            client.publish("GuardianBox/sonic-1-status", chamber1_state)
            print("publishing for chamber1")
    
        previous_message = chamber1_state
        time.sleep(0.5)

def check_chamber2():
    global chamber2_state

    previous_message = None
    
    while True:
        distance = controller2.read_ultrasonic()
        if distance <= 26:
            print(f"Chamber 2 : Occupied with {distance}")
            chamber2_state = "Occupied"

        else:
            print(f"Chamber 2 : Vacant with {distance}")
            chamber2_state = "Vacant"

        if previous_message != chamber2_state:
            client.publish("GuardianBox/sonic-2-status", chamber2_state)
            print("publishing for chamber2")
    
        previous_message = chamber2_state
        time.sleep(0.5)
        
def get_logs():
    command =  f"SELECT * from logs"
    rows = insert_to_database(command, "QUERY")
    datas = {}
    count = 1
    for row in rows:
        data = {
            "id" : row[0],
            "chamber_id" : row[1],
            "time_open" : row[2].strftime("%d-%m-%Y %H:%M:%S"),
            "time_close" : row[3].strftime("%d-%m-%Y %H:%M:%S")
        }
        datas[count] = data
        count += 1

    print(datas)
    datas_json = json.dumps(datas)
    
    client.publish("GuardianBox/logs-database", datas_json)


light_led_1 = 4
ultra_pin_1 = 17
echo_pin_1 = 27

light_led_2 = 12
ultra_pin_2 = 16
echo_pin_2 = 20

def on_message(client, usrdata, message):
    print("Receive : " + str(message.payload.decode()) + "\n")
    val = json.loads(message.payload.decode())
    
    if val["key"] == 1:
        if chamber1_state == "Vacant":
            controller1.mag_unlock()
            time.sleep(3)
            controller1.mag_lock()
            print("1 come")
            controller1.turn_on()
        
    elif val["key"] == 2:
        if chamber2_state == "Vacant":
            controller1.mag_unlock()
            time.sleep(3)
            controller1.mag_lock()
            print("2 come")
            controller2.turn_on()

    else:
        timeOpen = val["timeopen"]
        timeClose = val["timeclose"]
        dt_o = datetime.fromtimestamp(timeOpen / 1000)
        dt_c = datetime.fromtimestamp(timeClose / 1000)

        readable_timestamp = dt_o.strftime('%Y-%m-%d %H:%M:%S')
        readable_timeclose = dt_c.strftime('%Y-%m-%d %H:%M:%S')

        openCrate(val["chamber"],readable_timestamp,readable_timeclose)
        print("Inserted to database")


def on_connect(client, usrdata, flags, rc):
    if rc == 0:
        print("Successfully Connected")
    else:
        print("Error")

client = mqtt.Client()

controller1 = Contoller(light_led_1,ultra_pin_1,echo_pin_1)
controller2 = Contoller(light_led_2,ultra_pin_2,echo_pin_2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.subscribe("GuardianBox/chamber-controller", 0)

client.loop_start()

controller1.mag_lock()
chamber1 = threading.Thread(target=check_chamber1).start()
chamber2 = threading.Thread(target=check_chamber2).start()

timestamp_val = 0
timeclose_val = 0
chamber = 0

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()
    
