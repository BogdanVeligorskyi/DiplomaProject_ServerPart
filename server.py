import socket
import datetime
import threading
import measurementsDb
import roomsDb
import sensorsDb

# connection data
HOST = "192.168.0.115"
PORT = 50020

# keywords
IP_ADDR = "IP-ADDRESS"
STEP = "STEP"
MEASUREMENTS = "MEASUREMENTS"
QUIT = "QUIT"
GET_DEVICES = "GET_DEVICES"
SEND_DEVICES = "SEND_DEVICES"
GET_SENSORS = "GET_SENSORS"
SEND_SENSORS = "SEND_SENSORS"
GET_MEASUREMENTS = "GET_MEASUREMENTS"
SEND_MEASUREMENTS = "SEND_MEASUREMENTS"
GET_ACTUAL = "GET_ACTUAL"
SEND_ACTUAL = "SEND_ACTUAL"


# run  server
def my_server(step):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server started to wait for the client")
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=client_handler, args=(conn, addr, step,)).start()


def find_all_rooms():
    results = roomsDb.select_all_devices_from_room_table()
    print("Total rows are ", len(results))
    if len(results) == 0:
        return None
    roomsStr = SEND_DEVICES + ":"
    for row in results:
        roomsStr += "id=" + str(row['id']) + ","
        roomsStr += "name=" + str(row['name']) + ","
        roomsStr += "device_ip=" + str(row['device_ip']) + ","
        roomsStr += "device=" + str(row['device']) + ";"
        print("Id: ", row['id'])
        print("Name: ", row['name'])
        print("IP: ", row['device_ip'])
        print("Device: ", row['device'])
        print("")
    roomsStr += "\n"
    return roomsStr

# check IP in database
def check_in_rooms_table(ip):
    results = roomsDb.select_devices_from_room_table()
    print("Total rows are ", len(results))
    for row in results:
        print("device_ip: ", row['device_ip'])
        print("Id: ", row['id'])
        if str(row['device_ip']) == ip:
            print("This IP was found in database!")
            return row['id']
    return None

# find all sensors of specific room in database
def find_all_sensors_of_room(room_id):
    results = sensorsDb.select_sensors_from_sensors_table(room_id)
    print("Total rows are ", len(results))
    list_sensors = []
    if len(results) == 0:
        return None
    for row in results:
        print("Id: ", row['id'])
        list_sensors.append(row['id'])
    return list_sensors

def find_all_sensors():
    results = sensorsDb.select_all_sensors_from_sensors_table()
    print("Total rows are ", len(results))
    if len(results) == 0:
        return None
    sensorsStr = SEND_SENSORS + ":"
    for row in results:
        sensorsStr += "id=" + str(row['id']) + ","
        sensorsStr += "room_id=" + str(row['room_id']) + ","
        sensorsStr += "name=" + str(row['name']) + ","
        sensorsStr += "measure=" + str(row['measure']) + ","
        sensorsStr += "measure_unit=" + str(row['measure_unit']) + ";"
        print("Id: ", row['id'])
        print("Room Id: ", row['room_id'])
        print("Name: ", row['name'])
        print("Measure: ", row['measure'])
        print("Measure unit: ", row['measure_unit'])
        print("")
        # list_sensors.append(row['id'])
    sensorsStr += "\n"
    return sensorsStr

# find all sensors of specific room in database
def find_all_measurements_of_sensor(sensor_id, datetime_1, datetime_2):
    results = measurementsDb.select_specific_measurements(sensor_id, datetime_1, datetime_2)
    print("Total rows are ", len(results))
    if len(results) == 0:
        return None
    measurementsStr = SEND_MEASUREMENTS + ":"
    for row in results:
        measurementsStr += "id=" + str(row['id']) + ","
        measurementsStr += "sensor_id=" + str(row['sensor_id']) + ","
        measurementsStr += "value=" + str(row['value']) + ","
        measurementsStr += "date_time=" + str(row['date_time']) + ";"

        #print("Id: ", row['id'])
        #print("Sensor Id: ", row['sensor_id'])
        #print("Value: ", row['value'])
        #print("Datetime: ", row['date_time'])
        #print("")
        # list_sensors.append(row['id'])
    measurementsStr += "\n"
    return measurementsStr

# find all sensors of specific room in database
def find_actual_measurements_of_sensor(room_id, sensors_num):
    results = measurementsDb.select_actual_measurements(room_id, sensors_num)
    print("Total rows are ", len(results))
    if len(results) == 0:
        return None
    measurementsStr = SEND_ACTUAL + ":"
    for row in results:
        measurementsStr += "id=" + str(row['id']) + ","
        measurementsStr += "sensor_id=" + str(row['sensor_id']) + ","
        measurementsStr += "value=" + str(row['value']) + ","
        measurementsStr += "date_time=" + str(row['date_time']) + ";"

        print("Id: ", row['id'])
        print("Sensor Id: ", row['sensor_id'])
        print("Value: ", row['value'])
        print("Datetime: ", row['date_time'])
        print("")
        # list_sensors.append(row['id'])
    measurementsStr += "\n"
    return measurementsStr

def client_handler(conn, addr, step):
    with conn:
        print('Connected by ', addr)
        while True:
            data = conn.recv(1024).decode('utf-8')
            sensors = []
            # if mobile device requests for all devices
            if str(data).startswith(GET_DEVICES):
                print("Mobile device requests all devices")
                rooms_str = find_all_rooms()
                if rooms_str is not None:
                    encoded_room_str = rooms_str.encode('utf-8')
                    conn.sendall(encoded_room_str)
                else:
                    conn.sendall("No devices".encode('utf-8'))

            # if mobile device requests for all sensors
            if str(data).startswith(GET_SENSORS):
                print("Mobile device requests all sensors")
                sensor_str = find_all_sensors()
                if sensor_str is not None:
                    encoded_sensor_str = sensor_str.encode('utf-8')
                    conn.sendall(encoded_sensor_str)
                else:
                    conn.sendall("No sensors".encode('utf-8'))

            # if mobile device requests for all measurements
            if str(data).startswith(GET_MEASUREMENTS):
                print("Mobile device requests all measurements")
                print("Received: " + str(data))
                sensor_id_str = str(data)
                sensor_id_str = sensor_id_str[sensor_id_str.index(":")+1:]
                strArr = sensor_id_str.split(",")
                print(sensor_id_str)
                sensor_id = int(strArr[0])
                datetime_1 = strArr[1]
                datetime_2 = strArr[2]
                measurement_str = find_all_measurements_of_sensor(sensor_id, datetime_1+"%", datetime_2+"%")
                if measurement_str is not None:
                    encoded_measurement_str = measurement_str.encode('utf-8')
                    conn.sendall(encoded_measurement_str)
                else:
                    conn.sendall("No measurements".encode('utf-8'))

            # if mobile device requests for actual measurements
            if str(data).startswith(GET_ACTUAL):
                print("Mobile device requests actual measurements")
                print("Received: " + str(data))
                room_id_str = str(data)
                room_id_str = room_id_str[room_id_str.index(":") + 1:]
                strArr = room_id_str.split(",")
                print(room_id_str)
                room_id = int(strArr[0])
                sensors_num = int(strArr[1])
                print(sensors_num)
                measurement_str = find_actual_measurements_of_sensor(room_id, sensors_num)
                if measurement_str is not None:
                    encoded_measurement_str = measurement_str.encode('utf-8')
                    conn.sendall(encoded_measurement_str)
                else:
                    conn.sendall("No measurements".encode('utf-8'))

            # if IP-ADDRESS received from client
            if str(data).startswith(IP_ADDR):
                print("RECEIVED from client: " + str(data))
                list_ip = data.split(":")
                ip = list_ip[1]
                room_id = check_in_rooms_table(ip)
                if room_id is not None:
                    print("Sending step (in seconds) to client")
                    step_data = STEP + ":" + step
                    encoded_step_data = step_data.encode('utf-8')
                    conn.sendall(encoded_step_data)
                else:
                    print("No such IP in database!")
                    conn.sendall(QUIT.encode('utf-8'))
                    break

            # if MEASUREMENTS received from client
            elif str(data).startswith(MEASUREMENTS):
                print("RECEIVED from client: " + str(data))
                list_measurements = data.split(",")
                i = 1
                sensors = find_all_sensors_of_room(room_id)
                if len(sensors) == 0:
                    print("No sensors were added in this room!")
                else:
                    while i <= len(sensors):
                        print("Measurement {0}: {1}".format(i, list_measurements[i]))
                        measurementsDb.insert_to_measurements_table(sensors[i - 1],
                                                                    list_measurements[i],
                                                                    str(datetime.datetime.now().strftime(
                                                                        "%d-%m-%Y %H:%M:%S")))
                        i += 1

        conn.close()