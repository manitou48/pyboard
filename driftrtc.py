# print millis every 5 seconds
import pyb
rtc=pyb.RTC()
l = pyb.LED(3)
while(1):
	l.toggle()
	x= rtc.datetime()
	ms =int( 1000 * ( x[4]*3600 + x[5]*60 + x[6] + (255-x[7])/256.))
	print(ms)
	pyb.delay(5000)

