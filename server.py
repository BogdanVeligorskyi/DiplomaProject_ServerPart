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

# run server
def my_server(step):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server started to wait for the client")
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=client_handler, args=(conn, addr, step,)).start()

# check existence of IP in database
def check_in_rooms_table(ip):
    results = roomsDb.select_id_and_ip_from_rooms_table()
    print("Total rows are ", len(results))
    for row in results:
        print("device_ip: ", row['device_ip'])
        print("Id: ", row['id'])
        if str(row['device_ip']) == ip:
            print("This IP was found in database!")
            return row['id']
    return None

# find all sensors` id of specific room in database
def find_all_sensors_id_of_room(room_id):
    results = sensorsDb.select_sensors_id_from_sensors_table(room_id)
    print("Total rows are ", len(results))
    list_sensors = []
    if len(results) == 0:
        return None
    for row in results:
        print("Id: ", row['id'])
        list_sensors.append(row['id'])
    return list_sensors

# find all rooms to send to mobile device
def find_all_rooms():
    results = roomsDb.select_all_devices_from_rooms_table()
    print("Total rows are ", len(results))
    if len(results) == 0:
        return None
    rooms_str = SEND_DEVICES + ":"
    for row in results:
        rooms_str += "id=" + str(row['id']) + ","
        rooms_str += "name=" + str(row['name']) + ","
        rooms_str += "device_ip=" + str(row['device_ip']) + ","
        rooms_str += "device=" + str(row['device']) + ";"
        print("Id: ", row['id'])
        print("Name: ", row['name'])
        print("IP: ", row['device_ip'])
        print("Device: ", row['device'])
        print("")
    rooms_str += "\n"
    return rooms_str

# find sensors data to send to mobile device
def find_all_sensors():
    results = sensorsDb.select_all_sensors_from_sensors_table()
    print("Total rows are ", len(results))
    if len(results) == 0:
        return None
    sensors_str = SEND_SENSORS + ":"
    for row in results:
        sensors_str += "id=" + str(row['id']) + ","
        sensors_str += "room_id=" + str(row['room_id']) + ","
        sensors_str += "name=" + str(row['name']) + ","
        sensors_str += "measure=" + str(row['measure']) + ","
        sensors_str += "measure_unit=" + str(row['measure_unit']) + ";"
    sensors_str += "\n"
    return sensors_str

# find all measurements of sensor in specific time interval
# to send to mobile device
def find_all_measurements_of_sensor(sensor_id, datetime_1, datetime_2):
    results = measurementsDb.select_measurements_in_interval(sensor_id, datetime_1, datetime_2)
    print("Total rows are ", len(results))
    if len(results) == 0:
        return None
    measurements_str = SEND_MEASUREMENTS + ":"
    for row in results:
        measurements_str += "id=" + str(row['id']) + ","
        measurements_str += "sensor_id=" + str(row['sensor_id']) + ","
        measurements_str += "value=" + str(row['value']) + ","
        measurements_str += "date_time=" + str(row['date_time']) + ";"
    measurements_str += "\n"
    return measurements_str

# find actual measurements of specific sensor in database
# to send to mobile device
def find_actual_measurements_of_sensor(sensor_id, sensors_num):
    results = measurementsDb.select_actual_measurements(sensor_id, sensors_num)
    print("Total rows are ", len(results))
    if len(results) == 0:
        return None
    measurements_str = SEND_ACTUAL + ":"
    for row in results:
        measurements_str += "id=" + str(row['id']) + ","
        measurements_str += "sensor_id=" + str(row['sensor_id']) + ","
        measurements_str += "value=" + str(row['value']) + ","
        measurements_str += "date_time=" + str(row['date_time']) + ";"
        print("Id: ", row['id'])
        print("Sensor Id: ", row['sensor_id'])
        print("Value: ", row['value'])
        print("Datetime: ", row['date_time'])
        print("")
    measurements_str += "\n"
    return measurements_str

# handle requests from clients
def client_handler(conn, addr, step):
    with conn:
        print('Connected by ', addr)
        while True:
            data = conn.recv(1024).decode('utf-8')
            # if mobile device requests for all devices
            if str(data).startswith(GET_DEVICES):
                print("Mobile device requests all devices")
                rooms_str = find_all_rooms()
                if rooms_str is not None:
                    conn.sendall(rooms_str.encode('utf-8'))
                else:
                    conn.sendall("No devices".encode('utf-8'))

            # if mobile device requests for all sensors
            if str(data).startswith(GET_SENSORS):
                print("Mobile device requests all sensors")
                sensor_str = find_all_sensors()
                if sensor_str is not None:
                    conn.sendall(sensor_str.encode('utf-8'))
                else:
                    conn.sendall("No sensors".encode('utf-8'))

            # if mobile device requests for all measurements
            if str(data).startswith(GET_MEASUREMENTS):
                print("Mobile device requests all measurements")
                print("Received: " + str(data))
                sensor_id_str = str(data)
                sensor_id_str = sensor_id_str[sensor_id_str.index(":")+1:]
                str_arr = sensor_id_str.split(",")
                print(sensor_id_str)
                sensor_id = int(str_arr[0])
                datetime_1 = str_arr[1]
                datetime_2 = str_arr[2]
                measurement_str = find_all_measurements_of_sensor(sensor_id, datetime_1+"%", datetime_2+"%")
                if measurement_str is not None:
                    conn.sendall(measurement_str.encode('utf-8'))
                else:
                    conn.sendall("No measurements".encode('utf-8'))

            # if mobile device requests for actual measurements
            if str(data).startswith(GET_ACTUAL):
                print("Mobile device requests actual measurements")
                print("Received: " + str(data))
                sensor_id_str = str(data)
                sensor_id_str = sensor_id_str[sensor_id_str.index(":") + 1:]
                str_arr = sensor_id_str.split(",")
                print(sensor_id_str)
                sensor_id = int(str_arr[0])
                sensors_num = int(str_arr[1])
                print(sensors_num)
                measurement_str = find_actual_measurements_of_sensor(sensor_id, sensors_num)
                if measurement_str is not None:
                    conn.sendall(measurement_str.encode('utf-8'))
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
                    conn.sendall(step_data.encode('utf-8'))
                else:
                    print("No such IP in database!")
                    conn.sendall(QUIT.encode('utf-8'))
                    break

            # if MEASUREMENTS received from client
            elif str(data).startswith(MEASUREMENTS):
                print("RECEIVED from client: " + str(data))
                list_measurements = data.split(",")
                i = 1
                sensors = find_all_sensors_id_of_room(room_id)
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