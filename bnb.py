import requests
import boto3
import base64
import json
import re
import time
from secret import keys_bnb
from secret.listings import airbnbAll
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from secret.urls_bnb import baseURL, refreshURL, refreshPayload, refreshContent

def getTodaysCheckins():
  authToken = get_secret()
  today = str(datetime.now()).split(" ")[0]  # YYYY-MM-DD
  startDate = str(datetime.now()-timedelta(days=10)).split(" ")[0]  # YYYY-MM-DD -10days

  url = f"{baseURL}?{airbnbAll}&start_date={startDate}&end_date={today}&include=guest"

  payload = {}
  headers = {
    'Content-Type': keys_bnb.contentType,
    'Authorization': f'Bearer {authToken}'
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
      obtain_token(True) # Making sure the refresh fn will recursively call this fn upon completion 
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

def get_secret():
    secret_name = "BNBKey"
    region_name = "us-east-2"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            tokenResponseUtf8 = (secret.encode('utf8'))
            jsonNewToken = json.loads(tokenResponseUtf8)
            authToken = jsonNewToken['authToken']
            return authToken

        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

def obtain_token(fromGetTodaysCheckins=False):
  url = "https://auth.smartbnb.io/oauth/token"
  payload = 'audience=api.smartbnb.io&grant_type=client_credentials'
  headers = {
    'Authorization': keys_bnb.refreshToken,
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  response = requests.request("POST", url, headers=headers, data = payload)
  tokenResponseUtf8 = (response.text.encode('utf8'))
  jsonNewToken = json.loads(tokenResponseUtf8)
  newRefreshedToken = jsonNewToken['access_token']

  secret_name = "BNBKey"
  region_name = "us-east-2"
  # Create a Secrets Manager client
  session = boto3.session.Session()
  client = session.client(
      service_name='secretsmanager',
      region_name=region_name
  )
  put_secret_value_response = client.put_secret_value(
          SecretId=secret_name,
          SecretString = f'{{"authToken": \"{newRefreshedToken}\" }}'

  )
  print ("Access Token Has Been Refreshed")
  if fromGetTodaysCheckins==True:
    return getTodaysCheckins()

# print (getTodaysCheckins())
