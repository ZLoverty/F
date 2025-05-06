"""
Arduino_reader.py
=================

This script reads the text from an Arduino line-by-line and print in a local file in append ("a") mode. The current time string is prefixed to each line for reference. 

Syntax
------

python Arduino_reader.py

Edit
----
* May 06, 2025: automatically detect the home directory and set the folder to save the file in the Pictures folder.
"""

import serial
import time
import os

serialCom = serial.Serial("COM4", 9600)
home = os.path.expanduser("~")
folder = os.path.join(home, "Pictures")

while True:
    s_bytes = serialCom.readline()
    decoded_bytes = s_bytes.decode("utf-8").strip("\r\n")
    print(decoded_bytes)
    with open(os.path.join(folder, "rec.txt"), "a") as f:
        f.write(time.asctime() + "," + decoded_bytes + "\n")