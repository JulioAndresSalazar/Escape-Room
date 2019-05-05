import ujson, urequests, utime, machine, urandom

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
        
#DO NOT CHANGE
#combos = [(white2, 250), (yellow2, 500), (red2, 750), (orange2, 1000)]
led = [white2, yellow2, red2, orange2]
freq = [250, 500, 750, 1000]

def ledCheck():
    print('Testing LEDs...')
    utime.sleep(0.5)
    for i in range(4):
        led[i].on()  
        utime.sleep(0.5)
        led[i].off()
        utime.sleep(0.5)
    utime.sleep(1)
        
ledCheck() #makes sure all LEDS are functioning
        
def cloudPut(urlValue, headers, propValue):
    print(urequests.put(urlValue,headers=headers,json=propValue).text)
    #requests.put(urlValue,headers=headers,json=propValue).text 
    
def beep(frequency):
    pwm.freq(frequency)
    for i in range(1024):
        pwm.duty(i)
        utime.sleep(0.001)
    for i in range(1023, -1, -1):
        pwm.duty(i)
        utime.sleep(0.001)    
#    j = 0   
#    while j <1:
#        for i in range(1024):
#            pwm.duty(i)
#            utime.sleep(0.001)
#        for i in range(1023, -1, -1):
#            pwm.duty(i)
#            utime.sleep(0.001)
#        j += 1
    pwm.deinit()

#takes in indeces for code
def masterLoop(a, b, c, d):
     while True: 
        if colors[a].value() == True: 
            print('correct')  
            utime.sleep(0.3)
            return True
        else:
            utime.sleep(0.3)
            return False
#        elif colors[b].value() == True or colors[c].value() == True or colors[d].value() == True:
#            utime.sleep(0.3)
#            return False 

def simonBeep(Color, frequency):
    Color.on()
    beep(frequency)
    Color.off()
    utime.sleep(2)

#def correctSong:
def randint(min, max):
        span = max - min + 1
        div = 0x3fffffff // span
        offset = urandom.getrandbits(30) // div
        val = min + offset
        return val
    
def codeLoop():
    while True:
        loop1 = masterLoop(0, 1, 2, 3)
        if loop1 == True:
            loop2 = masterLoop(1, 0, 2, 3)
            if loop2 == True:
                loop3 = masterLoop(2, 0, 1, 3)
                if loop3 == True:
                    loop4 = masterLoop(3, 0, 1, 2)
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
    beep(1000)
#
def simonOne():
    for i in range(3):
        index = randint(0,3)
        #print(type(index))
        print(index)
        simonBeep(led[index], freq[index]) 
        #simonBeep(yellow2, 500)
        #simonBeep(red2, 750)
        #simonBeep(orange2, 1000)
        utime.sleep(2)

#CHANGE AS NEEDED
#This section decides what the code is:
Color1 = white
Color2 = yellow
Color3 = red
Color4 = orange

#DO NOT CHANGE
colors = [Color1, Color2, Color3, Color4]
codeLoop()
#simonOne()



#frequency = 250
#while True:
#    beep(frequency)
#    if Code[0].value() == True:
#        frequency -= 50
#    if Code[1].value() == True:
#        frequency += 50
        


#print('updating...')
#cloudPut(urlValue, headers, propValue)
