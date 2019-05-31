import machine
import utime
import urequests
import ujson

#DO NOT CHANGE
#API Info
Key = "sfIbD4eYzaMBqna_rZW5XQL2BR77CLb2I4BDvI6uxt" #global
urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/" #global
headers = {"Content-Type":"application/json","Accept":"application/json","x-ni-api-key":Key} #global

# Initiate Variables
keys = ["SL", "LSSS", "LSLS", "LSS", "S", "SSLS", "LLS", "SSSS", "SS", "SLLL", "LSL", "SLSS", "LL", "LS", "LLL",
        "SLLS", "LLSL", "SLS", "SSS", "L", "SSL", "SSSL", "SLL", "LSSL", "LSLL", "LLSS"]

def cloudGet(tag):
    urlValue = urlBase + tag + "/values/current"
    value = urequests.get(urlValue,headers=headers).text
    data = ujson.loads(value)
    result = data.get("value").get("value")
    return result

def cloudPut(tag, tag_type, val):
    Value = val
    Type = tag_type
    propValue = {"value":{"type":Type,"value":Value}}
    urlValue = urlBase + tag + "/values/current"
    print(urequests.put(urlValue,headers=headers,json=propValue).text)
    #requests.put(urlValue,headers=headers,json=propValue).text 


button = machine.Pin(23, machine.Pin.IN) 
previous_state = 0 # Initializing FSR
code = "" # Shorts and Longs
password = "" # Password string
led = machine.Pin(21, machine.Pin.OUT)


# Dictionary lookup
morsecodedictionary = dict()

fin = open("morsecode.txt")
for line in fin:
    word = line.strip()
    key = word[0]
    value =word[1:]
    morsecodedictionary[key] = value

def morseCode():
    print('starting game')
    current_string = ''
    previous_state = False
    while True:
        current_state = button.value() 
        #current state = either True or False depending on if sensor is pressed
        if current_state != previous_state:
            # if different, then there has been a change
            # update the previous state for next loop iteration
            previous_state = current_state
            if current_state == 1:
                #print('On') #sensor went from "off" to "on"
                #start = utime.time()
                #beep(392)
                start = utime.ticks_ms()
                #print(start)
                #Beep here 
            elif current_state == 0:
                #end = utime.time()
                end = utime.ticks_ms()
                on_time = end - start
                #print('On time: ' + str(on_time))
                #print('Off') #sensor went from "on" to "off"
                if on_time > short_long_threshold:
                    print('L')
                    current_string += 'L'
                elif on_time < short_long_threshold:
                    print('S')
                    current_string += 'S'
                print('Current string: ' + str(current_string))
                check = current_string.find(code, 0, len(current_string))
                if check == -1: 
                    continue
                elif check != -1:
                    break
            #utime.sleep(0.001)

short_long_threshold = 185 #185 pretty good
code = ''
pre_code = cloudGet("MorseCodePassword")
for letter in pre_code:
    code_letter = morsecodedictionary[letter]
    code += code_letter
print('Code is: ' +str(code))    
while True:  
    status = cloudGet("MorseCode")  
    print(status)
    if status == "UNSOLVED":
        led.off()
        morseCode()
        print('Solved!')
        led.on()
        cloudPut("MorseCode", "STRING", "SOLVED")
    elif status == "SOLVED":
        print('waiting')
    utime.sleep(0.5)