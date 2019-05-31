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

def noteValue(): 
    #This function returns a note given the correct button is pressed
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
        else:
            continue

def noteCheck(line):
    #This function checks whether the button pressed is the correct one for a given music line 
    while True:
        note = noteValue() 
        if note == line[0]:
            return True 
        elif note != line[0]: 
            return False
        
def songCode(line):
    #This is the main function. Uses previous functions to run Music Box Puzzle
    original_line = line
    while True: 
        check = noteCheck(line) 
        for i in range(len(line)-1): 
            if check == True: 
                reordered_line = reorder(line)
                check = noteCheck(reordered_line) 
                line = reordered_line 
            elif check == False:
                line= original_line 
                break 
        if check == True: 
            break 
        elif check == False: 
            continue
    playSongLine(line2)
    playSongLine(line3)
    playSongLine(line4)

    
#Start of main loop
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

