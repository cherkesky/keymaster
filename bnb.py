import requests
import datetime
import json
from secret.keys_bnb import authToken, contentType
from secret.listings import airbnbAll
from secret.urls_bnb import baseURL

def getTodaysCheckins():
  date = str(datetime.datetime.now()).split(" ")[0]
  url = f"{baseURL}?{airbnbAll}&start_date={date}&end_date={date}&include=guest"

  payload = {}
  headers = {
    'Content-Type': contentType,
    'Authorization': authToken
    }
  response = requests.request("GET", url, headers=headers, data = payload)

  utf8Response = response.text.encode('utf8')
  jsonResponse = json.loads(utf8Response)
  # print (utf8Response)

  checkinDict ={}
  checkinList =[]

  for guest in jsonResponse:
    if guest=="_pagination": 
      break
    checkinDict['listing'] = jsonResponse['data'][0]['listing_id']
    checkinDict['checkin'] = jsonResponse['data'][0]['check_in'].split('T')[0]
    checkinDict['checkout'] = jsonResponse['data'][0]['check_out'].split('T')[0]
    checkinDict['name'] = jsonResponse['data'][0]['_included'][0]['data']['first_name']
    checkinDict['code'] = jsonResponse['data'][0]['_included'][0]['data']['phone'].split('-')[1]
    checkinList.append(checkinDict)
    print (checkinList)
  return (checkinList)
# print (getTodaysCheckins())

