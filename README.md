![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

# ADS1115 16-bit Four Channel ADC
The ADS1115 is a 16-bit, four channel Analog-to-Digital (ADC) converter.  It runs on I2C and can be reprogramed with 4 different addresses.  It has an accurate internal reference voltage and programable gain.  

## Python code for the Raspberry Pi
This is a very basic program to allow you to use the ADS1115 with a Raspberry Pi. It does not have any special features, but can easily be modified to include them.  It was tested on Python 3.10, but should easily work with later versions of Python.  It is coded assuming that the use of 2/3 gain and only single-shot reads.  

## SMBus
This program uses smbus.  Any recent version is likely to work as only basic functions are used.  

## Other Features
The ADS1115 has many other features that are not implemented, such as continuous reading and a data ready pin.  

This project is licensed under the terms of the MIT license.
