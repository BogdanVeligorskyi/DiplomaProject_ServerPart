import os
import pymysql

import connection
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
        run_menu()
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

# run menu
def run_menu():
    while True:
        os.system('clear')
        print("-----MICROCLIMATE SYSTEM-----")
        print()
        print("1. Run system (Запустити систему).")
        print("2. Show rooms (Переглянути всі кімнати).")
        print("3. Show sensors (Переглянути датчики).")
        print("4. Show measurements (Переглянути всі показання).")
        print("5. Add new room (Додати нову кімнату).")
        print("6. Add new sensor (Додати новий датчик).")
        print("7. Update room (Оновити дані про кімнату).")
        print("8. Update sensor (Оновити дані про датчик).")
        print("9. Delete room (Видалити кімнату).")
        print("10. Delete sensor (Видалити датчик).")
        print("11. Delete all data (Видалити всі дані).")
        print("12. Exit (Закінчити роботу).")

        print()

        answer = input("Enter your number of operation (Виберіть номер операції): ")
        if answer == "1":
            os.system('clear')
            return
        elif answer == "2":
            print()
            show_rooms()
            input("Press Enter to continue (Натисніть Enter для продовження)")
        elif answer == "3":
            print()
            id_param = input("Enter id of the room (Вкажіть id кімнати): ")
            show_sensors(id_param)
            input("Press Enter to continue (Натисніть Enter для продовження)")
        elif answer == "4":
            print()
            id_param = input("Enter id of the sensor (Вкажіть id датчика): ")
            show_measurements(id_param)
            input("Press Enter to continue (Натисніть Enter для продовження)")
        elif answer == "5":
            print()
            add_room()
            input("Press Enter to continue (Натисніть Enter для продовження)")
        elif answer == "6":
            print()
            id_param = input("Enter id of the room (Вкажіть id кімнати): ")
            add_sensor(id_param)
            input("Press Enter to continue (Натисніть Enter для продовження)")
        elif answer == "7":
            print()
            id_param = input("Enter id of the room (Вкажіть id кімнати): ")
            update_room(id_param)
            input("Press Enter to continue (Натисніть Enter для продовження)")
        elif answer == "8":
            print()
            id_param = input("Enter id of the sensor (Вкажіть id датчика): ")
            update_sensor(id_param)
            input("Press Enter to continue (Натисніть Enter для продовження)")
        elif answer == "9":
            print()
            id_param = input("Enter id of the room (Вкажіть id кімнати): ")
            delete_room(id_param)
            input("Press Enter to continue (Натисніть Enter для продовження)")
        elif answer == "10":
            print()
            id_param = input("Enter id of the sensor (Вкажіть id датчика): ")
            delete_sensor(id_param)
            input("Press Enter to continue (Натисніть Enter для продовження)")
        elif answer == "11":
            delete_db()
            input("Press Enter to exit (Натисніть Enter для виходу)")
            exit(0)
        elif answer == "12":
            os.system('clear')
            exit(0)
        else:
            print()
            print("Your number isn`t correct (Такий номер не існує)")
            print()
            input("Press Enter to continue (Натисніть Enter для продовження)")

# add new room (new device)
def add_room():
    room = input("Enter your room (вкажіть назву кімнати): ")
    width = input("Enter your room width in meters (вкажіть ширину кімнати у метрах): ")
    length = input("Enter your room length in meters (вкажіть довжину кімнати у метрах): ")
    height = input("Enter your room height in meters (вкажіть висоту кімнати у метрах): ")
    device = input("Enter name of this device (вкажіть назву цього пристрою): ")
    ip_address = input("Enter IP-address of this device (вкажіть ІР-адресу пристрою, який зчитує дані з датчиків): ")
    print()
    if room != "" and device != "" and ip_address != "" and isfloat(width) and isfloat(length) and isfloat(height):
        room_id = roomsDb.insert_to_rooms_table(room, float(width), float(length), float(height), float(width) * float(length),
                                  ip_address, device)
        print('Room was added successfully! (Кімнату додано успішно!)')
        print()
        print("Id: ", str(room_id))
        print("Name: ", str(room))
        print("IP: ", str(ip_address))
        print("Device: ", str(device))
        print("Width, m: ", str(width))
        print("Length, m: ", str(length))
        print("Height, m: ", str(height))
        print("Square, m2: ", str( float(width)*float(length) ))
        print("")
    else:
        print('Room wasn`t added! (Кімнату не було додано!)')
        print("")

# add new sensor (?)
def add_sensor(room_id):
    print()
    if not check_in_rooms_table(room_id):
        print('This id isn`t correct (Цей id не існує) !')
        print()
        return

    sensor_name = input("Enter name of model sensor (Вкажіть назву моделі датчика): ")
    sensor_measure = input("Enter measure of model sensor (Вкажіть величину, яку вимірює датчик): ")
    sensor_unit = input("Enter unit measure (Вкажіть позначення одиниці вимірювання): ")
    sensor_range_min = input("Enter range min of model sensor (Вкажіть мінімальне значення, яке фіксує датчик): ")
    sensor_range_max = input("Enter range max of model sensor (Вкажіть максимальне значення, яке фіксує датчик): ")
    print()
    if sensor_name != "" and sensor_measure != "" and sensor_unit != "" and (isfloat(sensor_range_min) or sensor_range_min.isnumeric()) and (isfloat(sensor_range_max) or sensor_range_max.isnumeric()):
        sensor_id = sensorsDb.insert_to_sensors_table(room_id, sensor_name, sensor_measure, sensor_unit, float(sensor_range_min), float(sensor_range_max))
        print('Sensor was added successfully! (Датчик додано успішно!)')
        print()
        print("Id: ", str(sensor_id))
        print("Room Id: ", str(room_id))
        print("Name: ", str(sensor_name))
        print("Measure: ", str(sensor_measure))
        print("Measure unit: ", str(sensor_unit))
        print("Range min: ", str(sensor_range_min))
        print("Range max: ", str(sensor_range_max))
        print("")
    else:
        print('Sensor wasn`t added! (Датчик не було додано!)')
        print("")

# show all rooms
def show_rooms():
    results = roomsDb.select_all_data_from_rooms_table()
    if len(results) == 0:
        print("No rooms were found (Кімнати не знайдено)!")
        print("")
    for row in results:
        print("Id: ", row['id'])
        print("Name: ", row['name'])
        print("IP: ", row['device_ip'])
        print("Device: ", row['device'])
        print("Width, m: ", row['width'])
        print("Length, m: ", row['length'])
        print("Height, m: ", row['height'])
        print("Square, m2: ", row['square'])
        print("")

# show all sensors of specific room
def show_sensors(id_param):
    results = sensorsDb.select_specific_sensors_from_sensors_table(id_param)
    print()
    if len(results) == 0:
        print("No sensors were found (Датчики не знайдено)!")
        print("")
    for row in results:
        print("Id: ", row['id'])
        print("Room Id: ", row['room_id'])
        print("Name: ", row['name'])
        print("Measure: ", row['measure'])
        print("Measure unit: ", row['measure_unit'])
        print("Range min: ", row['range_min'])
        print("Range max: ", row['range_max'])
        print("")

# show all measurements of specific sensor
def show_measurements(id_param):
    results = measurementsDb.select_specific_measurements_from_measurements_table(id_param)
    print()
    if len(results) == 0:
        print("No measurements were found (Показання не знайдено)!")
        print("")
    for row in results:
        print("Id: ", row['id'])
        print("Sensor Id: ", row['sensor_id'])
        print("Value: ", row['value'])
        print("Datetime: ", row['date_time'])
        print("")

# update specific room
def update_room(id_param):
    print()
    if not check_in_rooms_table(id_param):
        print('This id isn`t correct (Цей id не існує) !')
        print()
        return
    name = input("Enter your room (вкажіть назву кімнати): ")
    width = input("Enter your room width in meters (вкажіть ширину кімнати у метрах): ")
    length = input("Enter your room length in meters (вкажіть довжину кімнати у метрах): ")
    height = input("Enter your room height in meters (вкажіть висоту кімнати у метрах): ")
    ip_address = input("Enter IP-address of this device (вкажіть ІР-адресу пристрою, який зчитує дані з датчиків): ")
    device = input("Enter name of this device (вкажіть назву цього пристрою): ")
    print()
    if name != "" and device != "" and ip_address != "" and isfloat(width) and isfloat(length) and isfloat(height):
        roomsDb.update_in_rooms_table(id_param, name, float(width), float(length), float(height),
                                                float(width) * float(length),
                                                ip_address, device)
        print('Room was updated successfully! (Кімнату оновлено успішно!)')
        print("")
        print("Id: ", str(id_param))
        print("Name: ", str(name))
        print("IP: ", str(ip_address))
        print("Device: ", str(device))
        print("Width, m: ", str(width))
        print("Length, m: ", str(length))
        print("Height, m: ", str(height))
        print("Square, m2: ", str(float(width) * float(length)))
        print("")
    else:
        print('Room wasn`t updated! (Кімнату не було оновлено!)')
        print("")

# update specific sensor
def update_sensor(id_param):
    print()
    if not check_in_sensors_table(id_param):
        print('This id isn`t correct (Цей id не існує) !')
        print()
        return
    sensor_name = input("Enter name of model sensor (Вкажіть назву моделі датчика): ")
    sensor_measure = input("Enter measure of model sensor (Вкажіть величину, яку вимірює датчик): ")
    sensor_unit = input("Enter unit measure (Вкажіть позначення одиниці вимірювання): ")
    sensor_range_min = input("Enter range min of model sensor (Вкажіть мінімальне значення, яке фіксує датчик): ")
    sensor_range_max = input("Enter range max of model sensor (Вкажіть максимальне значення, яке фіксує датчик): ")
    print()
    if sensor_name != "" and sensor_measure != "" and sensor_unit != "" and (
            isfloat(sensor_range_min) or sensor_range_min.isnumeric()) and (
            isfloat(sensor_range_max) or sensor_range_max.isnumeric()):
        sensorsDb.update_in_sensors_table(id_param, sensor_name, sensor_measure, sensor_unit,
                                                      float(sensor_range_min), float(sensor_range_max))
        print('Sensor was updated successfully! (Датчик оновлено успішно!)')
        print()
        print("Id: ", str(id_param))
        print("Name: ", str(sensor_name))
        print("Measure: ", str(sensor_measure))
        print("Measure unit: ", str(sensor_unit))
        print("Range min: ", str(sensor_range_min))
        print("Range max: ", str(sensor_range_max))
        print("")
    else:
        print('Sensor wasn`t updated! (Датчик не було оновлено!)')
        print("")

# delete specific room
def delete_room(id_param):
    if not check_in_rooms_table(id_param):
        print('This id isn`t correct (Цей id не існує) !')
        print()
    else:
        roomsDb.delete_from_rooms_table(id_param)
        print('Room was deleted successfully (Кімната була видалена успішно)!')
        print()

# delete specific sensor
def delete_sensor(id_param):
    if not check_in_sensors_table(id_param):
        print('This id isn`t correct (Цей id не існує) !')
        print()
    else:
        sensorsDb.delete_from_sensors_table(id_param)
        print('Sensor was deleted successfully (Датчик був видалений успішно)!')
        print()

# delete all data from database
def delete_db():
    conn = connection.get_connection()
    cursor = conn.cursor()
    query = """
            DROP DATABASE microclimate_system
            """
    cursor.execute(query)
    conn.commit()

# check whether entered value is float or not
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# check if record with id_param exists in Rooms table
def check_in_rooms_table(id_param):
    results = roomsDb.select_all_id_from_rooms_table()
    if len(results) == 0:
        return False
    for row in results:
        if str(id_param) == str(row['id']):
            return True
    return False

# check if record with id_param exists in Sensors table
def check_in_sensors_table(id_param):
    results = sensorsDb.select_all_id_from_sensors_table()
    if len(results) == 0:
        return False
    for row in results:
        if str(id_param) == str(row['id']):
            return True
    return False
