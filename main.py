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

def openCrate():
    timestamp_val = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Open crate sum
    crateOpen = "t"
    chamber_id = str(input("Which chamber"))
    while crateOpen == "t":
        crateOpen = input("Still open? t/f >")
    timeclose_val = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    command = f"INSERT INTO logs (chamber_id,time_open, time_close) values ('{chamber_id}', '{timestamp_val}','{timeclose_val}')"
    insert_to_database(command,"INSERT")

# def check_if_item_inside(controller):
#     global chamber1_state
#     print("===Door unlocked===")
#     doorOpen = True
#     message = None
#     previous_message = None
#     while doorOpen:
#         distance = controller.read_ultrasonic()
#         print(distance)
#         if distance <= 28.4:
#             print("Occupied")
#             # print("====Door locked===")
#             message = "Occupied"
#             controller.mag_lock()
#         else:
#             print("vacant")
#             message = "Vacant"
#             controller.mag_unlock()

#         if previous_message != message:
#             client.publish("GuardianBox/sonic-1-status", message)
#             print("publishing")

#         previous_message = message

def check_chamber1():
    global chamber1_state

    previous_message = None
    while True:
        distance = controller1.read_ultrasonic()
        if distance <= 28.4:
            print("Chamber1: Occupied")
            chamber1_state = "Occupied"

        else:
            print("Chamber1: Vacant")
            chamber1_state = "Vacant"

        if previous_message != chamber1_state:
            client.publish("GuardianBox/sonic-1-status", chamber1_state)
        # print("publishing for chamber1")
    
        previous_message = chamber1_state

def check_chamber2():
    global chamber2_state

    previous_message = None
    while True:
        distance = controller2.read_ultrasonic()
        if distance <= 28.4:
            print("Chamber2: Occupied")
            chamber2_state = "Occupied"

        else:
            print("Chamber2: Vacant")
            chamber2_state = "Vacant"

        if previous_message != chamber2_state:
            client.publish("GuardianBox/sonic-2-status", chamber2_state)
        # print("publishing for chamber1")
    
        previous_message = chamber2_state
        
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
mag_pin_1 = 21

light_led_2 = 4
ultra_pin_2 = 20
echo_pin_2 = 16
mag_pin_2 = 21

controller1 = Contoller(light_led_1,ultra_pin_1,echo_pin_1,mag_pin_1)
controller2 = Contoller(light_led_2,ultra_pin_2,echo_pin_2,mag_pin_2)

def on_message(client, usrdata, message):
    print("Receive : " + str(message.payload.decode()) + "\n")
    if(message.payload.decode() == "1"):
        controller1.mag_unlock()
        time.sleep(3)
        controller1.mag_lock()
        print("1 come")
        
        # check_if_item_inside(controller1)
    elif(message.payload.decode() == "2"):
        controller1.mag_unlock()
        time.sleep(3)
        controller1.mag_lock()
        print("2 come")
        # check_if_item_inside(controller2)
    else:
        print("0 come")


def on_connect(client, usrdata, flags, rc):
    if rc == 0:
        print("Successfully Connected")
    else:
        print("Error")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.subscribe("GuardianBox/chamber-controller", 0)

client.loop_start()
opt = None
controller1.mag_lock()
chamber1 = threading.Thread(target=check_chamber1).start()
chamber2 = threading.Thread(target=check_chamber2).start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()
    
# while opt != 0:
#     client.loop_start()
#     # client.publish("GuardianBox/SonicSta", "hehe")
#     if opt == 1:
#         create_database()
#     elif opt == 2:
#         create_log_table()
#     elif opt == 3:
#         openCrate()
#     elif opt == 4:
#         controller1.turn_on()
#     elif opt == 5:
#         controller1.turn_off()
#     elif opt == 6:
#         check_if_item_inside(controller1)
#     elif opt == 7:
#         get_logs()
#     client.loop_stop()
#     opt = int(input("Menu: \n0.Exit\n1.Create DB \n2.Create Table\n3.Open Crate \n4.Turn on light \n5.Turn off light \n> "))
