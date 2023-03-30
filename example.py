#!/usr/bin/env python3

import ADS1115 as ADS

ads = ADS.ADS1115() # Default address is 0x48

"""
Convert the digital value to voltage.
"""
def adc2volts(reading):
	print(ads.get_max_voltage())
	return (reading/32767)*ads.get_max_voltage()

# Read Channel 0 with a gain of 2/3 (Default value)
print(f"Channel 0: {ads.read_adc(0)}")
print(f"Channel 0 in volts: {adc2volts(ads.read_adc(0))}")


for itr in [0,1,2,3]:
	print(f"Channel {itr}: {ads.read_adc(itr)}")
		

print(f"Differential (0 minus 1): {ads.read_adc_difference(0)}")
