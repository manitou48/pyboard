   IR remote for Sony

--- files ----
IRsony.py   receiver and trasmitter classes for Sony

IRsonytst.py  test IR receiver and IR LED

irsonypy.png  snapshot of logic analyzer with IR LED in front of receiver
              running IRsonytst.py, Sony POWER code 0xA9A 
        channel 0, pin X2 PWM out  to IR LED
		channel 1, IR receiver output (to pin X4) 
		channel 2, debug, pulse measures time in callback (30us to 78us)


----  reference ----

http://forum.micropython.org/viewtopic.php?t=671
   NEC IR remote example

http://forum.micropython.org/viewtopic.php?t=671
   PWM discussion

http://forum.micropython.org/viewtopic.php?t=671
   PWM, input capture

https://github.com/z3t0/Arduino-IRremote
   Arduino/Teensy IRremote libraray
