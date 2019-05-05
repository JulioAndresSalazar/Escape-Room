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
#orange2 = machine.Pin(0, machine.Pin.OUT, machine.Pin.PULL_UP)
#red2 = machine.Pin(16, machine.Pin.OUT)
#red2.off()
#yellow2 = machine.Pin(2, machine.Pin.OUT)
#yellow2.off()
#white2 = machine.Pin(5, machine.Pin.OUT)
        
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
    pwm.deinit()


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

def playSongLine(line):
    i = 0
    for i in range(len(line)):    
        beep(line[i])
        utime.sleep(0.01)
        i += 1
    utime.sleep(0.2)

#Happy Birthday Note Lines
line1 = [G, G, A, G, C, B]
line2 = [G, G, A, G, D, C] 
line3 = [G, G, G2, E, C, B, A]
line4 = [F, F, E, C, D, C]

def reorder(list):
    new = list[1:]
    new.append(list[0])
    return new

line = [G, G, A, G, C, B] #this is fed in, tells us what note order to play


def lineToCode(line):
    code = []
    for note in line:
        if note == G:
            code.append(white)
        elif note == A:
            code.append(yellow)
        elif note == B:
            code.append(red)
        elif note == C:
            code.append(orange)
    print(code)
    return code

color_code = lineToCode(line) #this is created, for sensing inputs

def colorToNote(color):
        if color == white:
            return G 
        elif color == yellow:
            return A
        elif color == red:
            return B
        elif color == orange:
            return C
        
#Right Code or Wrong Button
#Send True or False
def songLoop(color_code, line): #Try: what happens if number of loops is bigger than the length 
     while True: 
        if color_code[0].value() == True: #if the first index of color_code is True
            note = colorToNote(color_code[0])
            beep(note) #play the note that corresponds to that color
            print('correct')
            #utime.sleep(0.3) #no time means faster note playing
            return True
        elif color_code[1].value() == True:
            note = colorToNote(color_code[1])
            beep(note) #play the note that corresponds to that color
            return False
        elif color_code[2].value() == True:
            note = colorToNote(color_code[2])
            beep(note) #play the note that corresponds to that color
            return False
        elif color_code[3].value() == True:
            note = colorToNote(color_code[3])
            beep(note)
            return False
        elif color_code[4].value() == True:
            note = colorToNote(color_code[4])
            beep(note)
            return False
        elif color_code[5].value() == True:
            note = colorToNote(color_code[5])
            beep(note)
            return False
        elif color_code[6].value() == True:
            note = colorToNote(color_code[6])
            beep(note)
            return False
        else:
            utime.sleep(0.05)
            continue
    
#def songCode(color_code, line):
#    original = color_code #only runs once
#    original_line = line #only runs once
#    while True: 
#        print('start of loop...') 
#        print(original, original_line)
#        #loop = songLoop(original, original_line) 
#        for i in range(len(line)-1):
#            if loop == True: #if Loop good, run again
#                reordered_code = reorder(color_code) #reorder code
#                reordered_line = reorder(line) #reorder line
#                print(reordered_code, reordered_line) 
#                loop = songLoop(reordered_code, reordered_line) #loop runs again 
#                color_code = reordered_code
#                line = reordered_line
#            elif loop == False: #if first color bad, return to top of while loop
#                color_code = original
#                line= original_line
#                print('bad color...') 
#                break
#        if loop == True:
#            print('solved')
#            break
#        elif loop == False:
#            color_code = original
#            line = original_line
#            print('bad color, outside break')
#            continue
#    #utime.sleep(0.1) #change this? no time?
#    playSongLine(line2)
#    playSongLine(line3)
#    playSongLine(line4)

#Recieve texts and get clues 
#get 'GGGC'
#note decoder 
           
#songCode(color_code, line)


#def wrongButton(color_code):
#   number of steps = len(color_code) -1       
#len(color_code) - 1 
#if color_code[]
 
def noteValue(): #listens for button push
    while True:
        if white.value() == True:
            beep(G)
            return G
        if yellow.value() == True:
            beep(A)
            return A
        if red.value() == True:
            beep(B)
            return B
        if orange.value() == True:
            beep(C)
            return C
        else:
            utime.sleep(0.05)
            continue
        
#press button - beeps
#is this the right button?
#note = newLoop()
#is note equal to 1st element? then 

#while True:
##    for i in range()
  #  if note == line[0]

def noteCheck(line):
    while True: #while True
        note = noteValue() #let buttons beep
        if note == line[0]: #if the button pressed matches line[0]
            return True #return a True
        elif note != line[0]: #if button is NOT the one in code, wrong button
            return False
        
def songCodeTest(color_code, line):
    original = color_code #only runs once
    original_line = line #only runs once
    while True: 
        print('start of loop...') 
        print(original, original_line)
        check = noteCheck(line) 
        for i in range(len(line)-1):
            if check == True: #if Loop good, run again
                reordered_code = reorder(color_code) #reorder code
                reordered_line = reorder(line) #reorder line
                print(reordered_code, reordered_line) 
                check = noteCheck(reordered_line)  #loop runs again 
                #color_code = reordered_code
                line = reordered_line
            elif check == False: #if first color bad, return to top of while loop
                color_code = original
                line= original_line
                print('bad color...') 
                break
        if check == True:
            print('solved')
            break
        elif check == False:
            color_code = original
            line = original_line
            print('bad color, outside break')
            continue
    #utime.sleep(0.1) #change this? no time?
    playSongLine(line2)
    playSongLine(line3)
    playSongLine(line4)
    
songCodeTest(color_code, line)
#i = 0
#while True:
#    note = newLoop
#    for i in range(1):
#        if note == line[i]:
#            print('Correct')
#            break
#        elif note != line[i]:
#            print('Incorrect')
#            break
#    break
#
#        
#print('updating...')
#cloudPut(urlValue, headers, propValue)
