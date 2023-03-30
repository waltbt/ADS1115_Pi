#!/usr/bin/env python3

"""
ADS1115.py
Function: A simple class to operate an ADS1115 over I2C on an RPi with Python
ADS1115 is 4 channel a 16-bit ADC which operates over I2C
Author: Benjamin Walt
Date: 3/30/2023
Version: 0.1
Copyright (c) Benjamin Thomas Walt
Licensed under the MIT license.
"""

import smbus
import time


# Register and other configuration values:
ADS1115_CONVERSION_REG     = 0x00
ADS1115_CONFIG_REG         = 0x01

# Gain values to config register values dictionary.
ADS1115_GAIN = {
    2/3: 0x00,
    1:   0x01,
    2:   0x02,
    4:   0x03,
    8:   0x04,
    16:  0x05
}

# Data rate to config register values dictionary.
ADS1115_DATA_RATE = {
    8:    0x00,
    16:   0x01,
    32:   0x02,
    64:   0x03,
    128:  0x04,
    250:  0x05,
    475:  0x06,
    860:  0x07
}


"""
Appropriate voltage ranges for gains
2/3: +/-6.144V
1: +/-4.096V
2: +/-2.048V
4: +/-1.024V
8: +/-0.512V
16: +/-0.256V
"""

ADS1115_GAIN2VOLTAGE = {
	2/3: 6.144,
	1: 4.096,
	2: 2.048,
	4: 1.024,
	8: 0.512,
	16: 0.256,
}


class ADS1115:
	"""ADS1115 analog to digital converter"""
	def __init__(self, address = 0x48):
		self._bus = smbus.SMBus(1) # Channel = 1
		self._address = address
		self._gain = 2/3 # 2/3 is good for values up to +/-6.144V
		self._data_rate = 128
	

	def _write_block(self, reg, data):
		"""Write a block of data to the device at the given register."""
		self._bus.write_i2c_block_data(self._address, reg, data)


	def _read_block(self, reg, data_size):
		"""Read a block of data from the device at the given register."""
		return self._bus.read_i2c_block_data(self._address, reg, data_size)
	

	def read_adc(self, channel):
		"""Read a single shot of a given channel compared to ground.
		Returns a 16-bit signed integer 0-32,767"""
		assert 0 <= channel <= 3, "ADS1115: Invalid channel."
		return self._read(channel + 0x04) # Bit 3 set high compares given channel to ground
	
	"""
	Supposedly, this will be less noisy to read than a single read
	"""
	def read_adc_difference(self, differential):
		"""Read the difference between two channels.
		Returns a 16-bit signed integer 0-32,767"""
		"""
		Differential input values:
		  0: Channel 0 minus channel 1
		  1: Channel 0 minus channel 3
		  2: Channel 1 minus channel 3
		  3: Channel 2 minus channel 3
		"""
		assert 0 <= differential <= 3, "ADS1115: Invalid differential value."
		return self._read(differential)


	def _read(self, mux):
		"""Read a single shot of the provided channel/differential"""
		"""
		D0:1 - COMP_QUE - Disabled (b11)
		D2 - COMP_LAT - Not used
		D3 - COMP_POL - Not used
		D4 - COMP_MODE - Not used
		D5:7 - DR (Data Rate)
		D8 - MODE 
		D9-11 - PGA (Gain)
		D12:14 - MUX
		D15 - OS (Operational status)
		"""
		# Set up the value to send to the config register
		config = 0x01 << 15 # Start a single conversion.
		config |= (mux & 0x07) << 12 # Select the channel to be read
		config |= (ADS1115_GAIN[self._gain]) << 9 # Set the gain
		config |= 0x01 << 8 # Set the mode to single shot
		config |= ADS1115_DATA_RATE[self._data_rate] << 5 # Set the data rate
		config |= 0x03  # Disable comparator mode.
		# Start the conversion.
		self._write_block(ADS1115_CONFIG_REG, [(config >> 8) & 0xFF, config & 0xFF])
		
		# Wait for conversion based on sample rate
		time.sleep(1.0/self._data_rate + 0.0001)
		
		# Read results from conversion register.
		raw_result = self._read_block(ADS1115_CONVERSION_REG, 2)
		# Combine for a 16 bit value
		value = ((raw_result[0] & 0xFF) << 8) | (raw_result[1] & 0xFF)
		# Check sign bit value
		if value & 0x8000 != 0:
			value -= 1 << 16
		return value
		
		
	def set_data_rate(self, rate):
		"""Sets the data rate"""
		if rate not in ADS1115_DATA_RATE:
			raise ValueError("ADS1115: Not a valid data rate")
		self._data_rate = rate
		
	def set_gain(self, gain):
		"""Sets the gain value"""
		if gain not in ADS1115_GAIN:
			raise ValueError("ADS1115: Not a valid gain value")
		self._gain = gain

	def get_data_rate(self):
		"""Returns the current data rate"""
		return self._data_rate
		
	def get_gain(self):
		"""Returns the current gain"""
		return self._gain
		
	def get_max_voltage(self):
		"""Return the max voltage for the current gain"""
		return ADS1115_GAIN2VOLTAGE[self._gain]
