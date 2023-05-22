import http.client

import pymysql
import measurementsDb
import roomsDb
import sensorsDb

conn = pymysql.connect(host='127.0.0.1',
                       user='Bogdan',
                       password='pwd_9')

# create new database 'microclimate_system'
def create_db(sensor):
    try:
        cursor = conn.cursor()
        query = """
                SELECT SCHEMA_NAME FROM
                INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'microclimate_system'
                """
        cursor.execute(query)
        # if database doesn`t exist - create it
        if cursor.fetchone() is None:
            first_time_init(cursor, sensor)
        update_devices()
        conn.commit()
    finally:
        conn.close()

# basic initialization: adding first room and all built-in sensors in Raspberry Pi
def first_time_init(cursor, sensor):
    query = """
            CREATE DATABASE microclimate_system
            """
    cursor.execute(query)
    conn.commit()
    roomsDb.create_rooms_table()
    print()
    print('Looks like you are running system for the first time.')
    print('Схоже, Ви вперше запустили цю систему.')
    room = input("Enter your room (вкажіть назву кімнати): ")
    width = input("Enter your room width in meters (вкажіть ширину кімнати у метрах): ")
    length = input("Enter your room length in meters (вкажіть довжину кімнати у метрах): ")
    height = input("Enter your room height in meters (вкажіть висоту кімнати у метрах): ")
    device = input("Enter name of this device (вкажіть назву цього пристрою): ")
    ip_address = input("Enter IP-address of this device (вкажіть ІР-адресу пристрою, який зчитує дані з датчиків): ")
    room_id = roomsDb.insert_to_rooms_table(room, float(width), float(length), float(height), float(width) * float(length),
                                  ip_address, device)
    dht_name = ""
    if sensor==11:
        dht_name = "DHT11"
    elif sensor==22:
        dht_name = "DHT22"
    else:
        dht_name = "DHT2302"
    sensorsDb.create_sensors_table()
    sensorsDb.insert_to_sensors_table(int(room_id), dht_name, "Temperature", "Cels", 0, 50)
    sensorsDb.insert_to_sensors_table(int(room_id), dht_name, "Humidity", "%", 20, 90)
    sensorsDb.insert_to_sensors_table(int(room_id), "MQ-135", "CO", "ppm", 0, 555)
    measurementsDb.create_measurements_table()
    print('First time initialization completed! (Початкова ініціалізація завершена!)')
    print()

# add new device(s) (room(s))
def update_devices():
    is_add = input('Do you want to add new device/room (Чи Ви хочете додати новий пристрій/кімнату) [Y/N]?')
    while is_add == "Y" or is_add == "y":
        add_new_room()
        is_add = input('Do you want to add new device/room (Чи Ви хочете додати новий пристрій/кімнату) [Y/N]?')

# add new room (new device)
def add_new_room():
    room = input("Enter your room (вкажіть назву кімнати): ")
    width = input("Enter your room width in meters (вкажіть ширину кімнати у метрах): ")
    length = input("Enter your room length in meters (вкажіть довжину кімнати у метрах): ")
    height = input("Enter your room height in meters (вкажіть висоту кімнати у метрах): ")
    device = input("Enter name of this device (вкажіть назву цього пристрою): ")
    ip_address = input("Enter IP-address of this device (вкажіть ІР-адресу пристрою, який зчитує дані з датчиків): ")
    room_id = roomsDb.insert_to_rooms_table(room, float(width), float(length), float(height), float(width) * float(length),
                                  ip_address, device)
    is_more = input("Is there any more model sensors? (Чи є ще моделі датчиків?) [Y/N]")
    while is_more == "Y" or is_more == "y":
        add_new_sensor(room_id)
        is_more = input("Is there any more model sensors? (Чи є ще моделі датчиків?) [Y/N]")
    print('Room was added successfully! (Кімнату додано успішно!)')

# add new sensor
def add_new_sensor(room_id):
    model_sensor_name = input("Enter name of model sensor (Вкажіть назву моделі датчика): ")
    model_sensor_measure = input("Enter measure of model sensor (Вкажіть величину, яку вимірює датчик): ")
    model_sensor_unit = input("Enter unit measure (Вкажіть позначення одиниці вимірювання): ")
    model_range_min = input("Enter range min of model sensor (Вкажіть мінімальне значення, яке фіксує датчик): ")
    model_range_max = input("Enter range max of model sensor (Вкажіть максимальне значення, яке фіксує датчик): ")
    sensorsDb.insert_to_sensors_table(room_id, model_sensor_name, model_sensor_measure, model_sensor_unit, model_range_min, model_range_max)
    print('Sensor was added successfully! (Датчик додано успішно!)')

