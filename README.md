# Microclimate Monitoring System (Server app on Python)

![alt text](https://github.com/BogdanVeligorskyi/DiplomaProject_ServerPart/blob/main/screens/screen_1.png?raw=true)
![alt text](https://github.com/BogdanVeligorskyi/DiplomaProject_ServerPart/blob/main/screens/screen_3.png?raw=true)
![alt text](https://github.com/BogdanVeligorskyi/DiplomaProject_ServerPart/blob/main/screens/screen_2.png?raw=true)
![alt text](https://github.com/BogdanVeligorskyi/DiplomaProject_ServerPart/blob/main/screens/screen_4.png?raw=true)

Application for Raspberry Pi devices which is used for control microclimate monitoring system.

## Features

1. Console user interface.
2. Start/stop measurements.
3. Turn on/off sound alarm.
4. Add, edit delete components (sensors, rooms).

## Available languages

English, Ukrainian

## Used technologies

Python 3.9, PyCharm Professional (2021.3.1), MariaDB, Raspberry Pi OS.

## How to run application

In order to run this application you have to connect all needed sensors (DHT11 and MQ-135) to Raspberry Pi. 
After that, make sure that your network address is static. And, run system by command (as example):

'python3 main.py <DHT sensor> <GPIO> <alarm> <time> <quickstart>' ('python3 main.py 11 4 on 15 off).

- DHT sensor may be: DHT11, DHT22 or DHT2302;
- GPIO is pin on RPi, connected to DHT sensor;
- alarm determines wheteher sound is on/off;
- time is decimal integer which equals to delay between two consistent measurements;
- quickstart option allows us (when on) to simply run the server without entering main menu.

NOTE: client application shows only last saved measurements if it`s not connected to server. 

## Demonstrational video

[YouTube (Ukrainian)](https://www.youtube.com/watch?v=2OtiZmEgbjE)

