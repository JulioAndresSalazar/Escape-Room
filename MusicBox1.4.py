import ujson, urequests, utime, machine

# Info
Tag = "LED"
Type = "INT"
Value = "1"
Key = "sfIbD4eYzaMBqna_rZW5XQL2BR77CLb2I4BDvI6uxt"

urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     
## PUT
urlTag = urlBase + Tag
urlValue = urlBase + Tag + "/values/current"

headers = {"Accept":"application/json","x-ni-api-key":Key}
propName={"type":Type,"path":Tag}
propValue = {"value":{"type":Type,"value":Value}}

#PUT Code
#requests.put(urlValue,headers=headers,json=propValue).text 
def cloudPut(urlValue, headers, propValue):
    print(urequests.put(urlValue,headers=headers,json=propValue).text)

#14, 12, 13, 15 are the pins in use
#all jumper cables for sensing are connected to positive side of LED

#This section defines pins as inputs DO NOT CHANGE
orange = machine.Pin(14, machine.Pin.IN)
red = machine.Pin(12, machine.Pin.IN)
yellow = machine.Pin(13, machine.Pin.IN)
white = machine.Pin(15, machine.Pin.IN)

#This section decides what the code is:
Color1 = white
Color2 = yellow
Color3 = red
Color4 = orange

#Define functions 
#numbers = ['1','2','3','4']
            
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

t = 0.3
while True:
    #loop1 is true or false
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
        #if loop 2 bad, rerun loop1
        continue

#Start SImo Says
print('updating...')
cloudPut(urlValue, headers, propValue)
