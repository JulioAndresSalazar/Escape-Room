#Import necessary libraries 
import ujson, urequests, utime, machine, urandom

#API Info
Key = "sfIbD4eYzaMBqna_rZW5XQL2BR77CLb2I4BDvI6uxt" 
urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/" 
headers = {"Content-Type":"application/json", "Accept":"application/json","x-ni-api-key":Key} 

def cloudGet(tag_name):
    #This function returns the tag value from the cloud
    urlValue = urlBase + tag_name + "/values/current"
    value = urequests.get(urlValue,headers=headers).text
    data = ujson.loads(value)
    result = data.get("value").get("value")
    return result

def cloudPut(tag, tag_type, val):
    #This function updates the tag value in the cloud
    Value = val
    Type = tag_type
    propValue = {"value":{"type":Type,"value":Value}}
    urlValue = urlBase + tag + "/values/current"
    print(urequests.put(urlValue,headers=headers,json=propValue).text)
    
#Pin setup    
lock = machine.Pin(23, machine.Pin.OUT)
lock.value(0)

#Start of main loop
#The processor constantly  reads the tag value. When the puzzle is unsolved it keeps the box closed. When the puzzle is solved
#the solenoid engages and unlocks the box
while True:
    status = cloudGet("LEDPuzzle")
    end = utime.time()
    print('Pin value: ' + str(lock.value()))
    print('Status: ' + str(status))
    print('Minutes since start: ' + str((end - start)/60.0) +'\n')
    if status == "SOLVED" and lock.value() == 0:
        print('solved')
        lock.on()
    elif status == "UNSOLVED" and lock.value() == 1:
        print('waiting...')
        lock.off()
    else:
        utime.sleep(0.5)
    utime.sleep(0.5)    
