# check RTC crystal drift with callback each second
# long time measurment of RTC drift
#  MCU cyrstal (micros()) has its own drift
import pyb
ticks =0
us=0
rtc = pyb.RTC()

def cb(exti):
	global ticks, us
	us = pyb.micros()
	ticks += 1


t0=0
nexttick = 5
rtc.wakeup(1000, cb)
while(1):
	if (ticks == nexttick) :
		t = ticks*1000000
		rt = t-t0
		t=us-us0      # rollover?
		ppm = 1.e6*(rt - t)/t
		print (ticks,t, rt, ppm, ' ppm')
		nexttick = ticks + 5
	if (ticks and t0 == 0):
		us0 = us
		t0 = ticks*1000000
		print(t0,us0)

