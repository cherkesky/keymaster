import requests, json, datetime
from secret.devices import listinglocks
from secret.urls_wink import baseURL
from secret.keys_wink import authToken, contentType
from bnb import getTodaysCheckins


dummydata = [{'name': 'GuyCh', 'code': '1173', 'checkin': '2020-06-25',
    'checkout': '2020-06-25', 'locks': ['257145']}]

today = str(datetime.datetime.now()).split(" ")[0]

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
    for guest in workorder:
        locks = guest['locks']
        guestCode = guest['code']
        guestName = guest['name']
        guestCheckIn = guest['checkin']
        if guestCheckIn==today:
          print ("Boop Boop - Codes Are Being Programmed...")
          for lock in locks:
              try:
                url = f"{baseURL}/locks/{lock}/keys"
                payload = f"{{\n    \"code\": \"{guestCode}\", \n    \"name\": \"{guestName}\"\n    }}"
                headers = {
                'Content-Type': contentType,
                'Authorization': authToken
                }

                # requests.request("POST", url, headers=headers, data = payload)
                print("------------------------------------------------------")
                print ("POST request for: ", guestName)
                print ("url: ", url)
                print ("payload: ", payload)
                print("------------------------------------------------------")
                print("DONE")

              except Exception as e:
                print(e)
        else: print ("No codes to program today")

def deleteCodes(workorder):
  for guest in workorder:
    locks = guest['locks']
    for lock in locks:
      print ("Lock: ", lock)
      url = f"{baseURL}/locks/{lock}/keys"
      guestName = guest['name']
      guestCheckOut = guest['checkout']
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
        if key['name'] == guestName and guestCheckOut==today:
          print ("Boop Boop - Codes Are Being Deleted...")
          try:
            url = f"{baseURL}/keys/{key['key_id']}"
            headers = {
            'Content-Type': contentType,
            'Authorization': authToken
            }

            # requests.request("DELETE", url, headers=headers, data = payload)
            print("------------------------------------------------------")
            print ("DELETE request for: ", guestName)
            print ("Checking Out At: ", guestCheckOut)
            print ("url: ", url)
            print ("payload: ", payload)
            print ("name: ",key['name'])
            print ("key_id: ", key['key_id'])
            print("------------------------------------------------------")
            print("DONE")

          except Exception as e:
            print(e)
        else: print (key['name'], "Doesnt need to be deleted today")
      

# programCodes(makeWorkOrder())
# deleteCodes(makeWorkOrder())

# programCodes(dummydata)
# deleteCodes(dummydata)
