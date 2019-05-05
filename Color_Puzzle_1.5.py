import ujson, urequests, utime, machine

#DO NOT CHANGE
#API Info
Tag = "LED"
Type = "INT"
Value = "1"
Key = "sfIbD4eYzaMBqna_rZW5XQL2BR77CLb2I4BDvI6uxt"
urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
urlTag = urlBase + Tag
urlValue = urlBase + Tag + "/values/current"
headers = {"Accept":"application/json","x-ni-api-key":Key}
propName={"type":Type,"path":Tag}
propValue = {"value":{"type":Type,"value":Value}}

#14, 12, 13, 15 are digital read 
#0, 16, 2, 5 are digital output
#4 is speaker pwm

#DO NOT CHANGE 
#This section defines pins as inputs
orange = machine.Pin(14, machine.Pin.IN)
red = machine.Pin(12, machine.Pin.IN)
yellow = machine.Pin(13, machine.Pin.IN)
white = machine.Pin(15, machine.Pin.IN)
pwm = machine.PWM(machine.Pin(4))

#DO NOT CHANGE
#This section defines digital output pins
orange2 = machine.Pin(0, machine.Pin.OUT, machine.Pin.PULL_UP)
red2 = machine.Pin(16, machine.Pin.OUT)
red2.off()
yellow2 = machine.Pin(2, machine.Pin.OUT)
yellow2.off()
white2 = machine.Pin(5, machine.Pin.OUT)

#PUT Code
#requests.put(urlValue,headers=headers,json=propValue).text 
def cloudPut(urlValue, headers, propValue):
    print(urequests.put(urlValue,headers=headers,json=propValue).text)

#use 250, 500, 750, 1000
def beep(frequency):
    pwm.freq(frequency)
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

def masterLoop(Color1, Color2, Color3, Color4, t):
     while True: 
        if Color1.value() == True: 
            print('correct 1')  
            utime.sleep(t)
            return True
        elif Color2.value() == True or Color3.value() == True or Color4.value() == True:
            #print('wrong button ' + numbers[j]+ 'st loop')
            utime.sleep(t)
            return False #reruns master loop if other buttons are pressed

def loopTwo(Color1, Color2, Color3, Color4, t):
     while True: 
        if Color2.value() == True: 
            print('correct 2')  
            utime.sleep(t)
            return True
            #break #only exit this loop if color2 is pressed
        elif Color1.value() == True or Color3.value() == True or Color4.value() == True:
            #print('wrong button ' + numbers[j]+ 'nd loop. Rerunning master loop')
            utime.sleep(t)
            return False
        
def loopThree(Color1, Color2, Color3, Color4, t):
     while True: 
        if Color3.value() == True: 
            print('correct 3')  
            utime.sleep(t)
            return True
            #break #only exit this loop if color2 is pressed
        elif Color1.value() == True or Color2.value() == True or Color4.value() == True:
            #print('wrong button ' + numbers[j]+ 'rd loop. Rerunning master loop')
            utime.sleep(t)
            return False
        
def loopFour(Color1, Color2, Color3, Color4, t):
     while True: 
        if Color4.value() == True: 
            print('correct 4')  
            utime.sleep(t)
            return True
            #break #only exit this loop if color2 is pressed
        elif Color1.value() == True or Color2.value() == True or Color3.value() == True:
            #print('wrong button ' + numbers[j]+ 'th loop. Rerunning master loop')
            utime.sleep(t)
            return False


def simonBeep(Color, frequency):
    Color.on()
    beep(frequency)
    Color.off()
    utime.sleep(t_beep)
    
#CHANGE AS NEEDED
#This section decides what the code is:
Color1 = white
Color2 = yellow
Color3 = red
Color4 = orange

def codeLoop():
    while True:
        loop1 = masterLoop(Color1, Color2, Color3, Color4, t)
        if loop1 == True:
            loop2 = loopTwo(Color1, Color2, Color3, Color4, t)
            if loop2 == True:
                loop3 = loopThree(Color1, Color2, Color3, Color4, t)
                if loop3 == True:
                    loop4 = loopFour(Color1, Color2, Color3, Color4, t)
                    if loop4 == True:
                        break
                    elif loop4 == False:
                        continue
                elif loop3 == False:
                    continue
            elif loop2 == False:
                continue
        elif loop1 == False:
            continue

#Start of script
t = 0.3
codeLoop()

t_beep = 0.5
while True:
    if Color3.value() == 1 or Color4.value() ==1:
        break
    else:
        simonBeep(orange2, 250) #3 but 2 
        simonBeep(red2, 500)
        simonBeep(yellow2, 750)
        simonBeep(white2, 1000)
        utime.sleep(2)
        
#as soon as button is pressed, begin waiting sequence like above i.e loops.

#print('updating...')
#cloudPut(urlValue, headers, propValue)
