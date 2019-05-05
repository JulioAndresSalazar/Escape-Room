import urequests, ujson

#DO NOT CHANGE
#API Info needed for both Get and Put
Key = "sfIbD4eYzaMBqna_rZW5XQL2BR77CLb2I4BDvI6uxt" #global
urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/" #global
headers = {"Accept":"application/json","x-ni-api-key":Key} #global
#"Content-Type":"application/json"

#Gets tage value
def cloudGet(tag_name):
    urlValue = urlBase + tag_name + "/values/current"
    value = urequests.get(urlValue,headers=headers).text
    data = ujson.loads(value)
    result = data.get("value").get("value")
    return result

#Updates tag in cloud
def cloudPut(tag, tag_type, val):
    Value = val
    Type = tag_type
    propValue = {"value":{"type":Type,"value":Value}}
    urlValue = urlBase + tag + "/values/current"
    print(urequests.put(urlValue,headers=headers,json=propValue).text)
    
cloudPut("LEDPuzzle", "STRING", "JulioTest")