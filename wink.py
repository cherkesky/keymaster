import requests, json, datetime
from secret.devices import listinglocks
from secret.urls_wink import baseURL
from secret.keys_wink import authToken, contentType
from bnb import getTodaysCheckins, get_secret

today = str(datetime.datetime.now()).split(" ")[0] #  'YYYY-MM-DD'

def makeWorkOrder():
    TodaysCheckins = getTodaysCheckins()

    if TodaysCheckins == 404: # No guest activity today
      workOrderList = 404
      return workOrderList  
    elif TodaysCheckins == None: # Happens sometimes after refreshing the bnb auth token
        print ("Something didnt work. Trying again..")
        TodaysCheckins = getTodaysCheckins()
        if TodaysCheckins == 404: # No guest activity today
          workOrderList = 404
          return workOrderList
    else:
        workOrderList = []
        for checkin in TodaysCheckins:
            workOrderDict = {}
            workOrderDict['name'] = checkin['name']
            workOrderDict['code'] = checkin['code']
            workOrderDict['checkin'] = checkin['checkin']
            workOrderDict['checkout'] = checkin['checkout']
            workOrderDict['locks'] = listinglocks[checkin['listing']]
            workOrderList.append(workOrderDict)
        return workOrderList

def programCodes(workorder):
  print ("Work Order: ",workorder)
  if workorder==404:
    print ("No guest activity today")
  else:
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

                requests.request("POST", url, headers=headers, data = payload)
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
  print ("Work Order: ",workorder)
  if workorder==404:
      print ("No guest activity today")
  else:
    for guest in workorder:
      locks = guest['locks']
      for lock in locks:
        print (f"\n","Lock: ", lock)
        print("------------------------------------------------------")
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

              requests.request("DELETE", url, headers=headers, data = payload)
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

