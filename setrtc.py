# set RTC from unix date 
# date +"%Y %m %d %w %H %M %S 0" > /dev/ttyACM0; echo "\r" > /dev/ttyACM0
import pyb
rtc = pyb.RTC()
print(rtc.datetime())
d = input('on unix date +"%Y %m %d %w %H %M %S 0"  > ')
d =  d.split()
d =  list(map(int,d))
if  d[3] == 0 :
	d[3]=7
print(d)
rtc.datetime(d)
print(rtc.datetime())
