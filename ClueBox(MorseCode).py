import ujson, urequests, utime, machine, urandom
#works on esp32

#DO NOT CHANGE
#API Info
Key = "sfIbD4eYzaMBqna_rZW5XQL2BR77CLb2I4BDvI6uxt" #global
urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/" #global
headers = {"Content-Type":"application/json", "Accept":"application/json","x-ni-api-key":Key} #global

def cloudGet(tag_name):
    urlValue = urlBase + tag_name + "/values/current"
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

lock = machine.Pin(23, machine.Pin.OUT)
lock.value(0)
start = utime.time()

while True:
    status = cloudGet("MorseCode")
    end = utime.time()
    print('Pin value: ' + str(lock.value()))
    print('Status: ' + str(status))
    print('Minutes since start: ' + str((end - start)/60.0) +'\n')
    if status == "1" and lock.value() == 0:
        #print('solved')
        lock.on()
    elif status == "0" and lock.value() == 1:
        #print('waiting...')
        lock.off()
    else: 
        utime.sleep(0.5)
    utime.sleep(0.5)    

print('Puzzle has been solved')    