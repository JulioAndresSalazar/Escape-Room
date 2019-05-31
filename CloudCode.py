#Import required libraries
import urequests, ujson

#NI Systenm Link Cloud API Info setup
Key = "sfIbD4eYzaMBqna_rZW5XQL2BR77CLb2I4BDvI6uxt" #global
urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/" #global
headers = {"Content-Type":"application/json", "Accept":"application/json","x-ni-api-key":Key} #global

def cloudGet(tag_name):
    #This function gets the tag value from the cloud
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
    
cloudGet("LEDPuzzle")
