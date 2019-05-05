#import machine, utime
#
#utime.sleep(5)
#p0 = machine.Pin(2)
#pwm0 = machine.PWM(p0)
#pwm0.freq(500)
#pwm0.duty(512)
#
#utime.sleep(7)
#pwm0.deinit()

import utime
import machine

pwm = machine.PWM(machine.Pin(4))

freq = 1000#750 #250#500 #lower frequency = lower note
def beep(freq):
    pwm.freq(freq)
    j = 0   
    while j <1:
        for i in range(1024):
            pwm.duty(i)
            utime.sleep(0.001)
        for i in range(1023, -1, -1):
            pwm.duty(i)
            utime.sleep(0.001)
        j += 1
    pwm.deinit()
beep(freq)