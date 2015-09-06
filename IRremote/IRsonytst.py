# IRsonytst.py for Sony  
#  xmit on X2  IR LED   timer5    pin-resistor-IRLED 
#  rcvr on X4  timer2    3.3v/grnd  e.g. TL1838 or GP1UX311QS
# http://forum.micropython.org/viewtopic.php?t=671
#  http://forum.micropython.org/viewtopic.php?t=542
# SONY  40khz, 12 bits

import pyb
import IRsony

mydata = 0

def sony_cb(sony, data) :
    global mydata
    mydata = data

sonyrcvr = IRsony.IRsony_rcvr()
sonyrcvr.callback(sony_cb)

sonyxmit = IRsony.IRsony_xmtr()

led = pyb.LED(4)
while True:
    print("sending SONY",hex(IRsony.SONY_BTN_POWER))
    sonyxmit.send(IRsony.SONY_BTN_POWER)
    if mydata :
        print("received",hex(mydata))
        mydata = 0
    led.on()
    pyb.delay(2000)
    led.off()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

