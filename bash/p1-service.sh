#!/bin/bash
stty -F /dev/ttyUSB0 115200
cat /dev/ttyUSB0 | /home/thomas/p1-sensor/env/bin/python /home/thomas/p1-sensor/src/p1-sensor.py
