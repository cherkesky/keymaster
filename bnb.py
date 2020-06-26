import requests
import datetime
import json
import re
import importlib
from secret import keys_bnb
from secret.listings import airbnbAll
from secret.urls_bnb import baseURL

def getTodaysCheckins():
  date = str(datetime.datetime.now()).split(" ")[0]
  url = f"{baseURL}?{airbnbAll}&start_date={date}&end_date={date}&include=guest"

  payload = {}
  headers = {
    'Content-Type': keys_bnb.contentType,
    'Authorization': keys_bnb.authToken
    }
  try:
    response = requests.request("GET", url, headers=headers, data = payload)
  except Exception as e:
    print(e)

  utf8Response = response.text.encode('utf8')
  jsonResponse = json.loads(utf8Response)
  print (jsonResponse)
  try:
    if jsonResponse['status_code']==401:
      print ("Token expired. Obtaining new Token")
      url = "https://auth.smartbnb.io/oauth/token"
      payload = 'audience=api.smartbnb.io&grant_type=client_credentials'
      headers = {
        'Authorization': keys_bnb.refreshToken,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
      response = requests.request("POST", url, headers=headers, data = payload)
      
      tokenResponseUtf8=(response.text.encode('utf8'))
      jsonNewToken = json.loads(tokenResponseUtf8)
      newRefreshedToken = jsonNewToken['access_token']

      print ("NEW TOKEN: ", newRefreshedToken)
      try:
        with open ('./secret/keys_bnb.py',"r+") as keyfile:
          keyfileContent = keyfile.read()
          keyfileContent = re.sub(f'authToken=\"(.*?)\"', f'authToken=\"Bearer {newRefreshedToken}\"', keyfileContent)
          keyfile.seek(0)
          keyfile.write (keyfileContent)
          keyfile.truncate()
          
      except FileNotFoundError:
        keyfileContent = None
      print (keyfileContent)
      importlib.reload(keys_bnb) # reloading the updated authToken resource
      getTodaysCheckins() # Lets try again. Now with a new token.

    else:
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
        # print (checkinList)
      return (checkinList)
  
  except Exception as e:
    print(e) 

print (getTodaysCheckins())
