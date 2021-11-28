# PID  DAC 12-bit and ADC 12-bit   DAC2 X6  ADC X19 
import pyb
from pyb import Pin,DAC, ADC

def doit(i):
	dac.write(i)
	v = i*vcc/4096
	a= adc.read()
	print(i,a,v)
	pyb.delay(5)

vcc = 3.3
dac = DAC(2, bits=12)
adc = ADC(Pin('X19'))
doit(2048)
doit(256)
#for i in range(256):     # check jitter
#    doit(2048)
# PID setup
delta_error = total_error = last_error = error = 0
limit = 4095
Kp = .1
Ki = .8
Kd = .0001
setpoint = 2048

for i in range(100):
    sensor = adc.read()
    error = setpoint - sensor
    total_error += error #accumalates the error - integral term
    if total_error >= limit:
		total_error = limit
    elif total_error <= -limit:
		total_error = -limit

    delta_error = error - last_error  #difference of error for derivative term

    control_signal = Kp * error + Ki * total_error + Kd  * delta_error
    if control_signal >= limit:
		 control_signal = limit
    elif control_signal < 0:
		 control_signal = 0

    last_error = error
    dac.write(int(control_signal + .5))
    print(error, delta_error, total_error, sensor, control_signal)
    pyb.delay(500)
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

