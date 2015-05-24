#  use timer2 instead of micros, SDIO disables IRQs
#  read write sectors  SD FLASH   SPI SD sd2
#  for sd  need to alter boot.py to not mount
import pyb
import os

# for SPI SD  need to manually :
#import sdcard
#sd = sdcard.SDCard(pyb.SPI(1), pyb.Pin.board.X5)
#sd = sdcard.SDCard(pyb.SPI(1), pyb.Pin.board.X5)   takes 2 times ?
#pyb.mount(sd, '/sd2')

# time open/io/close
def doio(blks) :

    os.remove(file)
    os.sync()
    print ("remove done, blocks",blks)

    t= t2.counter()
    f = open(file,'wb')
    for i in range(blks):
        f.write(buf)
    f.close()
    t= t2.counter() - t
    print ("all write",t,"us")

    t= t2.counter()
    f = open(file,'rb')
    for i in range(blks) :
        a=f.read(512)
    f.close()
    t= t2.counter() - t
    print ("all read",t,"us")
# verify last block
    errs=0
    for i in range(len(a)):
        if a[i] != i%256 :
            errs += 1
    print ("errs",errs)
    return


buf = bytearray(512)
for i in range(len(buf)) :
	buf[i]=i
file = '/flash/raw.dat'
#file = '/sd/raw.dat'
#file = '/sd2/raw.dat'
print (file)
t2 =  pyb.Timer(2, prescaler = 83, period = 0x3fffffff)
t2.counter(0)

f = open(file,'wb')
t= t2.counter()
f.write(buf)
t= t2.counter() - t
print ("write",t,"us")
t= t2.counter()
f.write(buf)
t= t2.counter() - t
print ("write",t,"us")
t= t2.counter()
f.write(buf)
t= t2.counter() - t
print ("write",t,"us")
f.seek(0)
t= t2.counter()
f.write(buf)
t= t2.counter() - t
print ("re write",t,"us")
f.close()

f = open(file,'rb')
t= t2.counter()
a=f.read(512)
t= t2.counter() - t
f.close()
print ("read",t,"us")

doio(40)
doio(20)
doio(10)
doio(3)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
