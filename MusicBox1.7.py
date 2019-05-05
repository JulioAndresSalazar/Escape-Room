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
        
#ledCheck() #makes sure all LEDS are functioning
        
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
        if led[a].value() == True: 
            print('correct')  
            utime.sleep(0.3)
            return True
        elif led[b].value() == True or led[c].value() == True or led[d].value() == True:
            utime.sleep(0.3)
            return False 

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
    print('starting simon')
#    utime.sleep(1)#tells user input was correct

def simonOne():
    i = 0
    for i in range(4):
        #index = randint(0,3)
        #print(type(index))
        #print(index)
        simonBeep(led[i], freq[i]) 
        #simonBeep(yellow2, 500)
        #simonBeep(red2, 750)
        #simonBeep(orange2, 1000)
        i += 1

#CHANGE AS NEEDED
#This section decides what the code is:
Color1 = white
Color2 = yellow
Color3 = red
Color4 = orange

#turn code into a list, and perform the codeLoop as many times as the length of the list

#DO NOT CHANGE
#colors = [Color1, Color2, Color3, Color4]
#codeLoop()
#simonOne()

#DO NOT CHANGE
#Note frequencies
G = 392
A = 440
B = 493
C = 523
D = 587
E = 659
F = 698
G2 = 783

#G G A G C B
#G G A G D C
#G G G E C B A 
#F F E C D C

def playSongLine(line):
    i = 0
    for i in range(len(line)):    
        beep(line[i])
        utime.sleep(0.5)
        i += 1
    
line1 =[G, G]#[G, G, A, G, C, B]
line2 = [G, G, A, G, D, C] 
line3 = [G, G, G2, E, C, B, A]
line4 = [F, F, E, C, D, C]

def songLoop(a, b, c, d, line):
     while True: 
        if led[a].value() == True: 
            beep(line[a])
            print('correct')
            utime.sleep(0.3)
            return True
        elif led[b].value() == True or led[c].value() == True or led[d].value() == True:
            utime.sleep(0.3)
            return False 

#def songCode():
##    while True:
##        for i in range(len(line1-1)): #led - 0 1 2 3 #note - 0 1 2 3 #runs 6 times 
#    loop = songLoop(0, 1, 2, 3, line1) #G is white 
#    return loop
            
def songCode():
    while True:
        for i in range(len(line1)):
            loop = songLoop(0, 1, 2, 3, line1)
            if loop == True: 
                loop = songLoop(1, 0, 2, 3, line1)
            elif loop == False:
                print('continuing....')
        if loop == True:
            print('solved')
            break
        elif loop == False:
            continue
        
songCode()
#playSongLine(line1)
#playSongLine(line2)
#playSongLine(line3)
#playSongLine(line4)

#frequency = 250
#while True:
#    print(frequency)
#    beep(frequency)
#    if led[0].value() == True:
#        frequency -= 50
#    if led[1].value() == True:
#        frequency += 50
        
#C =1046
#G = 783
#A =880
#B = 987
        
#print('updating...')
#cloudPut(urlValue, headers, propValue)
