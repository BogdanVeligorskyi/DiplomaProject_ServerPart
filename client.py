import random
import socket
import time

# network data
HOST = "192.168.0.115"
PORT = 50028

# keywords
IP_ADDR = "IP-ADDRESS"
STEP = "STEP"
MEASUREMENTS = "MEASUREMENTS"
SENSORS_NUM = 2

# imitate reading measurements from another device
def read_measurements_from_sensors():
    i = 0
    lst = [0, 1, 2, 3]
    random.shuffle(lst)
    measurements = ""
    temperature = lst[0] * 5 + 22
    humidity = lst[1] * 5 + 22
    lst = (temperature, humidity)
    while i < SENSORS_NUM:
        measurements = measurements + "," + str(lst[i])
        i += 1
    return measurements

# imitate work of another device
def my_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # try to connect and send IP for initialization
        s.connect((HOST, PORT))
        print("Client was connected: IP=192.168.0.116")
        my_ip = IP_ADDR + ":192.168.0.116"
        s.sendall(my_ip.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        while not str(data).startswith("QUIT"):
            # if received STEP - transfer measurements to server
            if str(data).startswith(STEP):
                lst = data.split(":")
                step = lst[1]
                print("RECEIVED from server: STEP:" + step)
                measurements = read_measurements_from_sensors()
                measurements_inp = MEASUREMENTS + measurements
                print(measurements_inp)
                measurements_enc = measurements_inp.encode('utf-8')
                s.sendall(measurements_enc)
                time.sleep(int(step))
        # if send IP was not found in database - disconnect
        if str(data).startswith("QUIT"):
            print("RECEIVED from server: this device has not been added yet!")
            s.close()

if __name__ == "__main__":
    my_client()