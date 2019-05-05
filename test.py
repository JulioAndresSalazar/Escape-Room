import json, requests, time#, machine, random

#DO NOT CHANGE
#API Info
Key = "sfIbD4eYzaMBqna_rZW5XQL2BR77CLb2I4BDvI6uxt" #global
urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/" #global
headers = {"Accept":"application/json","x-ni-api-key":Key} #global

#Updates tag in cloud
def cloudPut(tag, tag_type, val):
    Value = val
    Type = tag_type
    propValue = {"value":{"type":Type,"value":Value}}
    urlValue = urlBase + tag + "/values/current"
    print(requests.put(urlValue,headers=headers,json=propValue).text)
    
cloudPut("FinalBox", "STRING", "1")