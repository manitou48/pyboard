# pyboard micropython HTU21D temp/humidity I2C sensor
# https://www.sparkfun.com/products/12064 I2C   3.3v
# https://raw.githubusercontent.com/randymxj/Adafruit-Raspberry-Pi-Python-Code/master/Adafruit_HTU21D/Adafruit_HTU21D.py

import pyb

class HTU21D:
	i2c = None
  
	# HTU21D Address
	address = 0x40
	
	# Commands
	TRIGGER_TEMP_MEASURE_HOLD = 0xE3
	TRIGGER_HUMD_MEASURE_HOLD = 0xE5
	READ_USER_REG = 0xE7

	# Constructor
	def __init__(self):
		self.i2c = pyb.I2C(1, pyb.I2C.MASTER)
		
	def readUserRegister(self):
		#Read the user register byte
		return self.i2c.mem_read(1,self.address,self.READ_USER_REG)
	
	def readTemperatureData(self):
		#Read 3 temperature bytes from the sensor
		# value[0], value[1]: Raw temperature data
		# value[2]: CRC
		value = self.i2c.mem_read(3,self.address,self.TRIGGER_TEMP_MEASURE_HOLD)
		
		if not self.crc8check(value):
			return -255
			
		rawTempData = ( value[0] << 8 ) + value[1]
		
		rawTempData = rawTempData & 0xFFFC; # Clear the status bits
		
		# Calculate the actual temperature
		actualTemp = -46.85 + (175.72 * rawTempData / 65536)
		
		return actualTemp

	def readHumidityData(self):
		#Read 3 humidity bytes from the sensor
		# value[0], value[1]: Raw relative humidity data
		# value[2]: CRC
		value = self.i2c.mem_read(3,self.address,self.TRIGGER_HUMD_MEASURE_HOLD)
		
		if not self.crc8check(value):
			return -255

		rawRHData = ( value[0] << 8 ) + value[1]
		
		rawRHData = rawRHData & 0xFFFC; # Clear the status bits
		
		# Calculate the actual RH
		actualRH = -6 + (125.0 * rawRHData / 65536)
		
		return actualRH
	
	def crc8check(self, value):
		#Calulate the CRC8 for the data received
		# from https://github.com/sparkfun/HTU21D_Breakout
		remainder = ( ( value[0] << 8 ) + value[1] ) << 8
		remainder |= value[2]
		
		# POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
		# divsor = 0x988000 is polynomial shifted to farthest left of three bytes
		divsor = 0x988000
		
		for i in range(0, 16):
			if( remainder & 1 << (23 - i) ):
				remainder ^= divsor

			divsor = divsor >> 1
		
		if remainder == 0:
			return True
		else:
			return False
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
