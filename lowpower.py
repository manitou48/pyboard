# lowpower.py
# usb  frequency wfi stop standby    power: USB Vin 3.3v
#  GPIO pin config, what peripherals are enabled
import pyb
import stm

def dostop() :
    while True :
        # LPDS disable regulator, disable ADC DAC ?
        pyb.stop()      # pin interrupt or RTC could wake

def dostandby() :
    while True :
        pyb.standby()    # wakeup causes reset

def sleep() :
    while True :
        pyb.wfi()

def busy() :
    x=1
    while True:
        x = 1-x           # busy spin

#pyb.freq(84000000)     # default 168 try 84 42 24 8
#  disable some perihperals
#stm.mem32[stm.RCC + stm.RCC_AHB1ENR] = 0x100000   # GPIO  off
#stm.mem32[stm.RCC + stm.RCC_AHB2ENR] = 0  # USB OTG off
#stm.mem32[stm.RCC + stm.RCC_APB1ENR] = 0x10000000 # timers off
#stm.mem32[stm.RCC + stm.RCC_APB2ENR] =0x4000  # SDIO off
#pyb.usb_mode(None)   # this will kill ttyACM0 need to RST or cycle power

# tests  select 1

busy()     # spin 

#sleep()
#dostop()
#dostandby()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 

