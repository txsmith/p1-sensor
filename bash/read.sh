#!/bin/bash
stty -F /dev/ttyUSB0 115200
cat /dev/ttyUSB0 | /home/thomas/p1-sensor/go/parse/parse >> energy.log
