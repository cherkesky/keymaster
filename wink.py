import requests
from secret.devices import listinglocks
from secret.urls_wink import baseURL
from secret.keys_wink import authToken, contentType
from bnb import getTodaysCheckins


dummydata = [{'name': 'Test', 'code': '1173', 'checkin': '2020-06-25',
    'checkout': '2020-06-28', 'locks': ['257145']}]


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
              url = f"{baseURL}/{lock}/keys"
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

def deleteCodes():
    print("Boop Boop - Codes Has Been Deleted")


programCodes(makeWorkOrder())
# programCodes(dummydata)
