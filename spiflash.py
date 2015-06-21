# spiflash  SPI flash http://www.adafruit.com/product/1564 
# SPI 1 42mhz max   SPI 2  21 mhz max
# SPI1 X5-X8 CS CLK MISO MOSI   3.3v grnd
import pyb
from pyb import SPI
import ubinascii
import gc

CMD_JEDEC_ID = 0x9F
CMD_READ_STATUS = 0x05 # Read status register
CMD_READ = 0x03 # Read @ low speed
CMD_READ_HI_SPEED = 0x0B # Read @ high speed
CMD_WRITE_ENABLE = 0x06 # Write enable
CMD_PROGRAM_PAGE = 0x02 # Write page
CMD_ERASE_4k = 0x20
CMD_ERASE_32k = 0x52
CMD_ERASE_64k = 0xD8
CMD_ERASE_CHIP = 0xC7
CMD_READ_UID = 0x4B
PAGE_SIZE = 256

cmds = {'4k':CMD_ERASE_4k, '32k':CMD_ERASE_32k, '64k':CMD_ERASE_64k}

def read_block(addr,buff):
    cs.low()
    spi.send(CMD_READ)
    spi.send(addr>>16)
    spi.send(addr>>8)
    spi.send(addr)
    spi.recv(buff)
    cs.high()

def getid():
    cs.low()
    spi.send(CMD_JEDEC_ID)    # id
    r = spi.recv(3)
    cs.high()
    print (ubinascii.hexlify(r))

def wait():
  while True:
    cs.low()
    spi.send(CMD_READ_STATUS)
    r = spi.recv(1)[0]
    cs.high()
    if (r == 0) :
        return

def write_block(addr,buff):
    # write in 256-byte chunks
    # could check that doesn't go past end of flash ...
    length = len(buff)
    pos = 0
    while (pos < length):
        size = min(length-pos, PAGE_SIZE)
        cs.low()
        spi.send(CMD_WRITE_ENABLE)
        cs.high()

        cs.low()
        spi.send(CMD_PROGRAM_PAGE)
        spi.send(addr>>16)
        spi.send(addr>>8)
        spi.send(addr)
        spi.send(buff[pos:pos+size])
        cs.high()
        wait()
        addr += size
        pos += size

def erase(cmd,addr):
    cs.low()
    spi.send(CMD_WRITE_ENABLE)
    cs.high()
    cs.low()
    spi.send(cmds[cmd])
    spi.send(addr>>16)
    spi.send(addr>>8)
    spi.send(addr)
    cs.high()
    t = pyb.micros()
    wait()
    t = pyb.micros() - t
    print ("erase",cmd,t,'us')

def erase_chip():
    cs.low()
    spi.send(CMD_WRITE_ENABLE)
    cs.high()
    cs.low()
    spi.send(CMD_ERASE_CHIP)
    cs.high()
    t = pyb.micros()
    wait()
    t = pyb.micros() - t
    print ("erase chip",t)


print("SPI flash")
cs = pyb.Pin('X5')
cs.init(pyb.Pin.OUT_PP)
cs.high()
v = bytearray(4)
spi = SPI(1, SPI.MASTER, baudrate=42000000,polarity=0,phase=0)
wait()
getid()

buff = bytearray(32)
read_block(0,buff)
print (ubinascii.hexlify(buff))
read_block(12*600 +8,buff)    # paul's strings filenames
print (ubinascii.hexlify(buff))
print (buff)

erase('4k',524288)
#erase('32k',524288)
#erase('64k',524288)
#erase_chip()
wait()

buff = bytearray(256)
for i in range(len(buff)):
    buff[i] = i
t1 = pyb.micros()
write_block(524288,buff)
t2 = pyb.micros()
t=t2-t1
mbs = len(buff) * 8./t
print("write",len(buff),t,"us",mbs,"mbs ")

v = bytearray(256)
read_block(524288,v)
if (v == buff):
    print ("write/read ok")
else:
    print ("write/read FAILed")

gc.collect()
buff =bytearray(32*1024)
#buff =bytearray(64000)
t1 = pyb.micros()
read_block(0,buff)
t2 = pyb.micros()
t=t2-t1
mbs = len(buff) * 8./t
print("read",len(buff),t,"us",mbs,"mbs ")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
