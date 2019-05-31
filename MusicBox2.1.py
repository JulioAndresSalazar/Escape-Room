#Import necessary libraries
import ujson, urequests, utime, machine

#API Info Setup
Key = "sfIbD4eYzaMBqna_rZW5XQL2BR77CLb2I4BDvI6uxt" #global
urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/" #global
headers = {"Accept":"application/json","x-ni-api-key":Key} #global

def cloudPut(tag, tag_type, val):
    #This function updates a tag in the cloud
    Value = val
    Type = tag_type
    propValue = {"value":{"type":Type,"value":Value}}
    urlValue = urlBase + tag + "/values/current"
    print(urequests.put(urlValue,headers=headers,json=propValue).text)
    #requests.put(urlValue,headers=headers,json=propValue).text 

def cloudGet(tag):
    #This functions reads a tag value from the cloud
    urlValue = urlBase + tag + "/values/current"
    value = urequests.get(urlValue,headers=headers).text
    data = ujson.loads(value)
    result = data.get("value").get("value")
    return result

#This section initializes pins
blue = machine.Pin(16, machine.Pin.IN)
white = machine.Pin(15, machine.Pin.IN)
yellow = machine.Pin(13, machine.Pin.IN)
red = machine.Pin(12, machine.Pin.IN)
green = machine.Pin(14, machine.Pin.IN)
pwm = machine.PWM(machine.Pin(4))
        
def beep(frequency):
    #This function makes the speaker beep at a given frequency 
    pwm.freq(frequency)
    for i in range(1024):
        pwm.duty(i)
        utime.sleep(0.0001) #originaly 0.001
    for i in range(1023, -1, -1):
        pwm.duty(i)
        utime.sleep(0.0001) #originally 0.001 
    pwm.deinit()

def playSongLine(line):
    #This function plays any line of notes fed to it 
    i = 0
    for i in range(len(line)):    
        beep(line[i])
        utime.sleep(0.01)
        i += 1
    utime.sleep(0.2)

def reorder(list):
    #This function sends the first element of a list to end of list
    new = list[1:]
    new.append(list[0])
    return new

#Defines note frequencies
G = 392
A = 440
B = 493
C = 523
D = 587
E = 659
F = 698
G2 = 783

#Happy Birthday Note Lines for reference
line1 = [G, G, A, G, C, B]
line2 = [G, G, A, G, D, C] 
line3 = [G, G, G2, E, C, B, A]
line4 = [F, F, E, C, D, C]

def noteValue(): #listens for button push
    while True:
        if green.value() == True:
            beep(F)
            return F
        if red.value() == True:
            beep(G2)
            return G2
        if white.value() == True:
            beep(C)
            return C
        if yellow.value() == True:
            beep(D)
            return D
        if blue.value() == True:
            beep(G)
            return G
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


#cloudPut("LEDPuzzle", "STRING", "SOLVED")
#
#res = cloudGet("SongString")
#print(res)

while True:  
    status = cloudGet("LEDPuzzle")  
    print(status)
    if status == "UNSOLVED":    
        print('launching game...')
        song_line = []
        song_string = cloudGet("SongString") 
        print(song_string)
        for letter in song_string:
            if letter == 'G':
                song_line.append(G)
            if letter == 'A':
                song_line.append(A)
            if letter == 'B':
                song_line.append(B)            
            if letter == 'C':
                song_line.append(C)            
            if letter == 'D':
                song_line.append(D)
        print(song_line)
        print('Game start')
        songCode(song_line)
        print('Solved! Updating...')
        cloudPut("LEDPuzzle", "STRING", "SOLVED")
        #utime.sleep(1)
    elif status == "SOLVED":
        print('waiting')
        utime.sleep(1)





#def testLED(color):
#    while True:
#        if color.value() == 1:
#            print('high')
##            utime.sleep(0.5)
#        elif color.value() == 0:
#            print('low')
#            #utime.sleep(0.5)
            


