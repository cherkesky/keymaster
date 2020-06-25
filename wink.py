import requests, json
from secret.devices import listinglocks
from secret.urls_wink import baseURL
from secret.keys_wink import authToken, contentType
from bnb import getTodaysCheckins


dummydata = [{'name': 'Test', 'code': '1173', 'checkin': '2020-06-25',
    'checkout': '2020-06-26', 'locks': ['257145']}]


def makeWorkOrder():
    TodaysCheckins = getTodaysCheckins()
    workOrderDict = {}
    workOrderList = []
    for checkin in TodaysCheckins:
        workOrderDict['name'] = checkin['name']
        workOrderDict['code'] = checkin['code']
        workOrderDict['checkin'] = checkin['checkin']
        workOrderDict['checkout'] = checkin['checkout']
        workOrderDict['locks'] = listinglocks[checkin['listing']]
        workOrderList.append(workOrderDict)
    return workOrderList


def programCodes(workorder):
    print(workorder)
    for guest in workorder:
        locks = guest['locks']
        for lock in locks:
            try:
              url = f"{baseURL}/locks/{lock}/keys"
              guestCode = guest['code']
              guestName = guest['name']
              payload = f"{{\n    \"code\": \"{guestCode}\", \n    \"name\": \"{guestName}\"\n    }}"
              headers = {
              'Content-Type': contentType,
              'Authorization': authToken
              }

              requests.request("POST", url, headers=headers, data = payload)

              print ("url: ", url)
              print ("payload: ", payload)
              print("------------------------------------------------------")
            except Exception as e:
              print(e)

def deleteCodes(workorder):
  print(workorder)
  for guest in workorder:
    locks = guest['locks']
    for lock in locks:
      print (lock)
      url = f"{baseURL}/locks/{lock}/keys"
      guestName = guest['name']
      payload = {}
      headers = {
        'Content-Type': contentType,
        'Authorization': authToken
        }
      response = requests.request("GET", url, headers=headers, data = payload)
      utf8Response = response.text.encode('utf8')
      jsonResponse = json.loads(utf8Response)
      keys = jsonResponse['data']
      for key in keys:
        print ("name: ",key['name'])
        print ("key_id: ", key['key_id'])
        print("------------------------------------------------------")
        if key['name'] == guestName:
          try:
            url = f"{baseURL}/keys/{key['key_id']}"
            headers = {
            'Content-Type': contentType,
            'Authorization': authToken
            }

            requests.request("DELETE", url, headers=headers, data = payload)

            print ("url: ", url)
            print ("payload: ", payload)
            print("------------------------------------------------------")
          except Exception as e:
            print(e)

      

# programCodes(makeWorkOrder())
# programCodes(dummydata)
deleteCodes(dummydata)
# deleteCodes(makeWorkOrder())
