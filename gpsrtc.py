# GPS pps interrupt on X1
# long time measurment of RTC drift
import pyb
ticks =0
rtc = pyb.RTC()

def callback(line):
	global ticks
	ticks += 1

pin = pyb.Pin('X1')
pyb.ExtInt(pin, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_NONE, callback)

t0=0
rt0=0
nexttick = 5
while(1):
	if (ticks == nexttick) :
		us = ticks*1000000
		x= rtc.datetime()
		rt =  1000  * ( x[4]*3600 + x[5]*60 + x[6]) + (1000*(255-x[7]))/256
		rt = rt-rt0
		t=us-t0
		ppm = 1.e6 * (1000*rt - t)/t
		print (ticks,t, rt, ppm, ' ppm')
		nexttick = ticks + 5
	if (ticks and t0 == 0):
		x= rtc.datetime()
		rt0 =  1000  * ( x[4]*3600 + x[5]*60 + x[6]) + (1000*(255-x[7]))/256
		t0 = ticks*1000000
		print(t0,rt0)

