import ujson, urequests, utime, machine, urandom

#DO NOT CHANGE
#API Info
Tag = "LED"
Type = "INT"
Value = "1" #1 for solved. 0 for unsolved 
Key = "sfIbD4eYzaMBqna_rZW5XQL2BR77CLb2I4BDvI6uxt"
urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
urlTag = urlBase + Tag
urlValue = urlBase + Tag + "/values/current"
headers = {"Accept":"application/json","x-ni-api-key":Key}
propName={"type":Type,"path":Tag}
propValue = {"value":{"type":Type,"value":Value}}

#DO NOT CHANGE unless adding new color
#This section initializes pins
#16, 15, 13, 12, 14 are digital read 
#4 is speaker pwm
blue = machine.Pin(16, machine.Pin.IN)
white = machine.Pin(15, machine.Pin.IN)
yellow = machine.Pin(13, machine.Pin.IN)
red = machine.Pin(12, machine.Pin.IN)
green = machine.Pin(14, machine.Pin.IN)
#newcolor = machine.Pin(new pin, machine.Pin.IN)

#Defines speaker pwm pin
pwm = machine.PWM(machine.Pin(4))
        
#Updates tag in cloud
def cloudPut(urlValue, headers, propValue):
    print(urequests.put(urlValue,headers=headers,json=propValue).text)
    #requests.put(urlValue,headers=headers,json=propValue).text 
    
#Makes the speaker beep at a given frequency. Use note frequencies   
def beep(frequency):
    pwm.freq(frequency)
    for i in range(1024):
        pwm.duty(i)
        utime.sleep(0.0001) #originaly 0.001
    for i in range(1023, -1, -1):
        pwm.duty(i)
        utime.sleep(0.0001) #originally 0.001 
    pwm.deinit()

#Returns random integer(not working yet)
def randint(min, max):
        span = max - min + 1
        div = 0x3fffffff // span
        offset = urandom.getrandbits(30) // div
        val = min + offset
        return val

#Note frequencies
G = 392
A = 440
B = 493
C = 523
D = 587
E = 659
F = 698
G2 = 783

#This function plays any line of notes fed to it
def playSongLine(line):
    i = 0
    for i in range(len(line)):    
        beep(line[i])
        utime.sleep(0.01)
        i += 1
    utime.sleep(0.2)

#Happy Birthday Note Lines for reference
line1 = [G, G, A, G, C, B]
line2 = [G, G, A, G, D, C] 
line3 = [G, G, G2, E, C, B, A]
line4 = [F, F, E, C, D, C]

#Sends 0 element to end of list
def reorder(list):
    new = list[1:]
    new.append(list[0])
    return new

#CHANGE THIS AS NEEDED
#This is the code we feed in
#line = [G, G, A, G, C, B] 

def noteValue(): #listens for button push
    while True:
        if green.value() == True:
            beep(G)
            return G
        if red.value() == True:
            beep(A)
            return A
        if white.value() == True:
            beep(B)
            return B
        if yellow.value() == True:
            beep(C)
            return C
        if blue.value() == True:
            beep(D)
            return D
#         if newcolor.value() == True:
#            beep(newnote)
#            return newnote       
        else:
#            utime.sleep(0.05)
            continue

def noteCheck(line):
    while True: #while True
        note = noteValue() #let buttons beep
        if note == line[0]: #if the button pressed matches line[0]
            return True #return a True
        elif note != line[0]: #if button is NOT the one in code, wrong button
            return False
        
def songCode(line):
    original_line = line #creates variable of the song "code"
    while True: 
        check = noteCheck(line) #waits for buttons to be pushed. if correct button pushed, returns true
        for i in range(len(line)-1): #for the length of the note code...
            if check == True: #if the button pressed was correct:
                reordered_line = reorder(line) #reorder the code 
                check = noteCheck(reordered_line)  #waits for next button to be pressed 
                line = reordered_line #resets the variable and does it again
            elif check == False: #if at ANY time, the wrong buton is pressed...
                line= original_line #we reset the line variable..
                break #Then we break from the loop
        if check == True: #If we managed to put in all the correct color..
            break #we break from the second loop
        elif check == False: #If we input any wrong buttons, this value is False
            #line = original_line
            continue
    playSongLine(line2)
    playSongLine(line3)
    playSongLine(line4)
            
songCode(line1)

def testLED(color):
    while True:
        if color.value() == 1:
            print('high')
#            utime.sleep(0.5)
        elif color.value() == 0:
            print('low')
            #utime.sleep(0.5)
#testLED(green)
#Recieve texts and get clues 
#get 'GGGC'
#note decoder 
#print('updating...')
#cloudPut(urlValue, headers, propValue)
