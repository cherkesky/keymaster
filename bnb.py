import requests
import datetime
import json
from secret.keys import authToken, contentType
from secret.listings import airbnbAll
from secret.urls import baseURL

date = str(datetime.datetime.now()).split(" ")[0]
reservationsOf = '&listings[]='

url = f"{baseURL}?{airbnbAll}&start_date={date}&end_date={date}&include=guest"

payload = {}
headers = {
  'Content-Type': contentType,
  'Authorization': authToken
  }

response = requests.request("GET", url, headers=headers, data = payload)
utf8Response = response.text.encode('utf8')
jsonResponse = json.loads(utf8Response)

for guest in jsonResponse:
  if guest=="_pagination": 
    break
  print("Listing: ",jsonResponse['data'][0]['listing_id'])
  print("Check In: ",jsonResponse['data'][0]['check_in'].split('T')[0])
  print("Check Out: ",jsonResponse['data'][0]['check_out'].split('T')[0])
  print("Name: ",jsonResponse['data'][0]['_included'][0]['data']['first_name'])
  print("Code: ",jsonResponse['data'][0]['_included'][0]['data']['phone'].split('-')[1])
  print ("---")

# print (utf8Response)

