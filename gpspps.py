# GPS pps interrupt on X1
import pyb
tick =0
us = 0

def callback(line):
	global tick,us
	us=pyb.micros()
	tick=1

pin = pyb.Pin('X1')
pyb.ExtInt(pin, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_NONE, callback)

prev=0
while(1):
	if (tick) :
		t=us-prev
		print (t, t-1000000, ' ppm')
		tick = 0
		prev = us

