import os, json, requests, csv, threading

ak= os.environ.get("ACCESS_KEY")
secret = os.environ.get("SECRET")

def token():
    url="https://api4.prismacloud.io/login"
    payload={
        "username":ak,
        "password":secret
    }
    headers={
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8'
    }

    response=requests.request("POST",url,headers=headers,data=json.dumps(payload))
    response=json.loads(response.content)

    return response['token']

def asset_explorer(cloud,pageToken=""):
    url="https://api4.prismacloud.io/v2/resource/scan_info"
    if pageToken=="":
        payload={
            "cloud.type":cloud
        }
    else:
        payload={
            "cloud.type":cloud,
            "pageToken":pageToken
        }
    headers={
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token()
    }
    response=requests.request("GET",url,headers=headers,json=payload)
    response=json.loads(response.text)
    return response
    
data=asset_explorer("aws")
print(data['nextPageToken'])

counter=data['totalMatchedCount']
counter=counter/10000
counter=int(counter)
print(counter)
next_page_token=data['nextPageToken']
data_main=data['resources']
n=0

for x in range(counter):
    data=asset_explorer("aws",next_page_token)
    next_page_token=data['nextPageToken']
    data_main.append(data['resources'])
    n=n+1
    print(data['nextPageToken'])
    print(n)

fieldnames = list(data_main[0].keys())
with open("my_data.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for item in data_main:
      writer.writerow(item)
