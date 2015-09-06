# IRsony.py
#  SONY transmit on X2 (timer5 channel) PWM 40khz to IR LED
# SONY decode from IR rcvr on X4  timer2 channel 4 running at 1mhz
# ref   http://forum.micropython.org/viewtopic.php?t=671
#  http://forum.micropython.org/viewtopic.php?t=542
#  data from rcvr is inverted  mark==0
# SONY 40khz 12 bits  hdrmark 2400 space 600  mark 1200

import pyb
# buffer for traceback assistance in ISRs  callbacks
import micropython
micropython.alloc_emergency_exception_buf(100)


SONY_BITS = 12
SONY_FREQ = 40000
SONY_HDR_MARK = 2400
SONY_HDR_SPACE =600
SONY_ONE_MARK  =1200
SONY_ZERO_MARK =600

TOPBIT = 1 << (SONY_BITS-1)

# some sony buttons   12-bit codes
SONY_BTN_POWER = 0xa9a
SONY_BTN_PLAY = 0x18b
SONY_BTN_PAUSE = 0x70b
SONY_BTN_STOP = 0xf0b
SONY_BTN_1 = 0x01a
SONY_BTN_2 = 0x81a
SONY_BTN_3 = 0x41a

class IRsony_xmtr:
    def __init__(self, timer=5, channel=2, pin=pyb.Pin.board.X2):
        self._t = pyb.Timer(timer, freq=SONY_FREQ)
        self._tchnl = self._t.channel(channel,pyb.Timer.PWM, pin=pin, pulse_width_percent=0)


    def _mark(self, us):
        self._tchnl.pulse_width_percent(50)
        pyb.udelay(us)

    def _space(self, us):
        self._tchnl.pulse_width_percent(0)
        pyb.udelay(us)

    def send(self, data):
        self._mark(SONY_HDR_MARK)
        self._space(SONY_HDR_SPACE)
        for i in range(SONY_BITS):
            if data & TOPBIT :
                self._mark(SONY_ONE_MARK)
                self._space(SONY_HDR_SPACE)
            else:
                self._mark(SONY_ZERO_MARK)
                self._space(SONY_HDR_SPACE)
            data = data << 1


#debug_pin = pyb.Pin('X3', pyb.Pin.OUT_PP)

class IRsony_rcvr:
    def __init__(self, timer=2, channel=4, pin=pyb.Pin.board.X4):
        self._t = pyb.Timer(timer, prescaler=83, period=0x0fffffff)
        self._ic_pin = pin
        self._ic = self._t.channel(channel, pyb.Timer.IC, pin=self._ic_pin, polarity=pyb.Timer.BOTH)
        self._ic_start = 0
        self._ic_width = 0
        self._ic.callback(self._ic_cb)
        self._rst()
        self._cb = None
        
    def _rst(self):
        self._data = 0
        self._bits = 0      # total bits 
        
    def _bit(self, v):
		# collect bits, MSB 
        self._data = (self._data << 1) + v
        self._bits = self._bits + 1
        if ( self._bits >= SONY_BITS):     # data done
            if (self._cb):
                self._cb(self,  self._data) # release data
            self._rst()
            
    def _ic_cb(self, timer):
        #debug_pin.value(1)
        if self._ic_pin.value() == 0:
            # falling edge   rcvr inverted
            self._ic_start = self._ic.capture()
        else:
            # rising edge
            icw = self._ic.capture() - self._ic_start & 0x0fffffff
            self._ic_width = icw
            if (icw > 5000):
                #print('[gap]') # gap in transmission
                pass
            elif (icw > 2100):           # sony mark hdr  2400
                #print('IR start')
                self._rst()
            elif (icw > 1000):           # sony mark 1200
                self._bit(1)	# High bit
            else:
                self._bit(0) # Low bit
            
            #print(self._ic_start, self._ic_width)
        #debug_pin.value(0)

    def callback(self, fn):
        self._cb = fn

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
