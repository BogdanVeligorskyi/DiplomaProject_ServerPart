import random
import socket
import time

HOST = "localhost"
PORT = 50004

IP_ADDR = "IP-ADDRESS"
STEP = "STEP"
MEASUREMENTS = "MEASUREMENTS"
SENSORS_NUM = 2

def read_measurements_from_sensors():
    i = 0
    lst = [0, 1, 2, 3]
    random.shuffle(lst)
    measurements = ""
    temperature = lst[0]
    humidity = lst[1]

    lst = (temperature, humidity)
    while i < SENSORS_NUM:
        measurements = measurements + "," + str(lst[i])
        i += 1
    return measurements

# run client
def my_client():
    #threading.Timer(11, my_client).start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Client was connected: IP=192.168.1.116")
        my = IP_ADDR + ":192.168.1.116"
        my_inp = my.encode('utf-8')
        s.sendall(my_inp)
        data = s.recv(1024).decode('utf-8')
        # якщо отримано ПЕРІОД - передати показники серверу
        while not str(data).startswith("QUIT"):
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
        if str(data).startswith("QUIT"):
            print("RECEIVED from server: this device hasn`t been added yet!")
            s.close()

if __name__ == "__main__":
    my_client()