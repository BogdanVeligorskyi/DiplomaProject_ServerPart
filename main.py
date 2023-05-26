#!/usr/bin/python
# Python scripts for running Microclimate System.
import sys
import threading
import Adafruit_DHT
import datetime
import time

import server
import db
import measurementsDb
import RPi.GPIO as GPIO
from smbus import SMBus

# initialization of buzzer
def init_buzzer():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    buzzer = 16
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.output(buzzer, GPIO.LOW)
    return buzzer


# initialization of ADC
def init_adc():
    DEV_ADDR = 0x48
    adc_channel = 0b1000010 # 0x42 (input AIN2 for ADC)
    bus = SMBus(1)          # 1 - I2C bus address for RPi rev.2
    return DEV_ADDR, adc_channel, bus


# parsing command line parameters.
def read_command_line_params():
    # default time between two measurements, s
    step_s = 10
    is_alarm = "on"
    sensor_args = {'DHT11': Adafruit_DHT.DHT11,
                   'DHT22': Adafruit_DHT.DHT22,
                   'DHT2302': Adafruit_DHT.AM2302}
    # if only 3 arguments were written
    if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
        sensor = sensor_args[sys.argv[1]]
        pin = sys.argv[2]
    # if additional 4th argument was written
    elif len(sys.argv) == 4 and sys.argv[1] in sensor_args:
        sensor = sensor_args[sys.argv[1]]
        pin = sys.argv[2]
        step_s = (sys.argv[3])
    elif len(sys.argv) == 5 and sys.argv[1] in sensor_args:
        sensor = sensor_args[sys.argv[1]]
        pin = sys.argv[2]
        is_alarm = sys.argv[3]
        step_s = (sys.argv[4])
    else:
        print('ENGLISH description:')
        print('Usage: python3 main.py [DHT11|DHT22|DHT2302] <GPIO pin number> <alarm on/off> <step, s>')
        print('Example 1: python3 main.py DHT11 4 - '
              'Read from an DHT11 connected to GPIO pin #4')
        print('Example 2: python3 main.py DHT11 4 15 - '
              'Read each 15 seconds from an DHT11 connected to GPIO pin #4')
        print('---------------------------')
        print('УКРАЇНСЬКОЮ пояснення:')
        print('Застосування: python3 main.py [DHT11|DHT22|DHT2302] <GPIO номер виводу> <сигналізація on/off> <період, с>')
        print('Приклад 1: python3 main.py DHT11 4 - '
              'Прочитати дані з DHT11, підключеного до GPIO-виводу #4')
        print('Приклад 2: python3 main.py DHT11 4 on 15 - '
              'Зчитувати дані кожні ~15 секунд з DHT11, підключеного до GPIO-виводу #4 та увімкнутою сигналізацією')
        sys.exit(1)

    db.create_db(sensor)
    threading.Thread(target=server.my_server, args=(step_s,)).start()
    #server.my_server(step_s)

    return sensor, pin, is_alarm, step_s


# read current temperature and humidity
def read_from_dht(sensor, pin, current_datetime):

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        print(current_datetime.strftime("%d-%m-%Y %H:%M:%S") +
              ' Temp(температура)={0:0.1f}*C  Humidity(вологість)={1:0.1f}%'.
              format(temperature, humidity))
        measurementsDb.insert_to_measurements_table \
            (2, str(humidity),
             str(current_datetime.strftime("%d-%m-%Y %H:%M:%S")))
        measurementsDb.insert_to_measurements_table \
            (1, str(temperature),
             str(current_datetime.strftime("%d-%m-%Y %H:%M:%S")))
    else:
        print('Failed to read humidity or temperature data. Try again!')
        print('-------------------')
        print('Не вдалося визначити вологість повітря або температуру. Спробуйте ще!')


# read gas concentration from MQ-135 sensor using analog output
def read_from_mq_135(DEV_ADDR, adc_channel, bus, current_datetime, is_alarm):
    # read sensor value from ADC
    bus.write_byte(DEV_ADDR, adc_channel)
    bus.read_byte(DEV_ADDR)
    bus.read_byte(DEV_ADDR)
    value = bus.read_byte(DEV_ADDR)
    print(current_datetime.strftime("%d-%m-%Y %H:%M:%S") +
          ' CO Concentration(концентрація СО)={0}ppm'.format(value))
    measurementsDb.insert_to_measurements_table \
        (3, str(value),
         str(current_datetime.strftime("%d-%m-%Y %H:%M:%S")))

    # if concentration value is greater than 55 ppm and
    # turn on alarm
    if value > 55 and is_alarm=='on':
        GPIO.output(buzzer, GPIO.HIGH)
    elif value <= 55 and is_alarm=='on':
        GPIO.output(buzzer, GPIO.LOW)


buzzer = init_buzzer()
DEV_ADDR, adc_channel, bus = init_adc()
sensor, pin, is_alarm, step_s = read_command_line_params()

# reading temperature, humidity and CO concentration
# values each 'step_s' seconds
while 1:
    current_datetime = datetime.datetime.now()
    read_from_dht(sensor, pin, current_datetime)
    read_from_mq_135(DEV_ADDR, adc_channel, bus, current_datetime, is_alarm)
    time.sleep(int(step_s))
