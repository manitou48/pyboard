# use cpu clock millis() to check drift, LSI (RC) has big offset
# print millis every 5 seconds
import pyb
l = pyb.LED(3)
rtc=pyb.RTC()
#rtc.calibration(-200)    # units` val*.954 = ppm
m0 = pyb.millis()
x= rtc.datetime()
r0 =int( 1000 * ( x[4]*3600 + x[5]*60 + x[6] + (255-x[7])/256.))
ms=m0
rs=r0
for i in range(100):
	l.toggle()
	pyb.delay(5000)
        ms =  pyb.millis()
	x= rtc.datetime()
	rs =  int( 1000 * ( x[4]*3600 + x[5]*60 + x[6] + (255-x[7])/256.))
        ppm = int(1.e6*((rs-r0) - (ms-m0))/(ms-m0))
	print(ms-m0, rs-r0, ppm)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
