# wizntp   
#  ntp time base is 1900, posix 1970,  micropython 2000
import pyb
import network
import struct
import time

nic = network.WIZNET5K(pyb.SPI(1), pyb.Pin.board.X5, pyb.Pin.board.X4)
#nic.ifconfig(('192.168.1.16', '255.255.255.0', '192.168.1.1', '75.75.75.75'))
#pyb.delay(300)    # wait for ifconfig
rtc = pyb.RTC()

# now use socket as usual
from socket import *

TIME2000 = 3155702400 - 4*3600  # timezone
client = socket( AF_INET, SOCK_DGRAM )
query = bytearray(48)
query[0] = 0x1b
client.sendto( query, ( '192.168.1.4', 123 ))
data, address = client.recvfrom( 1024 )
t = struct.unpack( '!I', data[40:] )   # hack unpack for micropy
t = t[0]  - TIME2000
d = time.localtime(t)
rtc.datetime((d[0],d[1],d[2],1,d[3],d[4],d[5],0)) # set rtc day of week bogus
print ('rtc', rtc.datetime())
pyb.delay(5000)
print ('rtc', rtc.datetime())
