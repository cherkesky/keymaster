import requests
from datetime import datetime, timedelta
import json
import re
import importlib
import time
from secret import keys_bnb
from secret.listings import airbnbAll
from secret.urls_bnb import baseURL, refreshURL, refreshPayload, refreshContent

def getTodaysCheckins():
  today = str(datetime.now()).split(" ")[0]  # YYYY-MM-DD
  startDate = str(datetime.now()-timedelta(days=10)).split(" ")[0]  # YYYY-MM-DD -10days

  url = f"{baseURL}?{airbnbAll}&start_date={startDate}&end_date={today}&include=guest"

  payload = {}
  headers = {
    'Content-Type': keys_bnb.contentType,
    'Authorization': keys_bnb.authToken
    }
  try:
    response = requests.request("GET", url, headers=headers, data=payload)
  except Exception as e:
    print(e)
  utf8Response = response.text.encode('utf8')
  jsonResponse = json.loads(utf8Response)
  try:
    statusCode = 000  # initial value. might get changed by an error code
    try:
      statusCode = jsonResponse['status_code']
      print("Status Code: ", statusCode)
    except:
       print("Seems like everything is ok")
    if statusCode == 404:
      print ("No results found")
      return 404
    elif statusCode == 401:  # Unauthorized. Token expired. 
      print("Token expired. Obtaining new Token")
      getRefreshedToken()
    else: # All good. Token is still valid and valid data returned
      checkinList =[]
      for guest in jsonResponse['data']:
        checkinDict ={}
        if guest['status'] == "ACCEPTED":
          checkinDict['listing'] = guest['listing_id']
          checkinDict['checkin'] = guest['check_in'].split('T')[0]
          checkinDict['checkout'] = guest['check_out'].split('T')[0]
          checkinDict['name'] = guest['_included'][0]['data']['first_name']
          checkinDict['code'] = guest['_included'][0]['data']['phone'].split('-')[1]
          checkinList.append(checkinDict)
      if len(checkinList) == 0:
        return 404
      else: 
        print ("BNB Work Order: ",checkinList)
        return checkinList

  except Exception as e:
    print(e) 


def getRefreshedToken():
  url = refreshURL
  payload = refreshPayload
  headers = {
    'Authorization': keys_bnb.refreshToken,
    'Content-Type': refreshContent
  }
  response = requests.request("POST", url, headers=headers, data = payload)
  tokenResponseUtf8 = (response.text.encode('utf8'))
  jsonNewToken = json.loads(tokenResponseUtf8)
  newRefreshedToken = jsonNewToken['access_token']
  try:  # Updating the authToken value in the resource file
    with open('./secret/keys_bnb.py', "r+") as keyfile:
      keyfileContent = keyfile.read()
      keyfileContent = re.sub(
          f'authToken=\"(.*?)\"', f'authToken=\"Bearer {newRefreshedToken}\"', keyfileContent)
      keyfile.seek(0)
      keyfile.write(keyfileContent)
      keyfile.truncate()
  except FileNotFoundError:
    keyfileContent = None
  importlib.reload(keys_bnb)  # reloading the updated authToken resource
  print ("Access Token Has Been Refreshed")


# print (getTodaysCheckins())
