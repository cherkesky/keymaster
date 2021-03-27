import requests, json, datetime
import boto3
import base64
from secret.devices import listinglocks
from secret.devices import locks as lock_name
from secret.urls_wink import baseURL
from botocore.exceptions import ClientError
from secret.keys_wink import contentType,client_id,client_secret,refresh_token
from bnb import getTodaysCheckins, get_secret

today = str(datetime.datetime.now()).split(" ")[0] #  'YYYY-MM-DD'

def makeWorkOrder()->list:
  """
  Process a checkinList dictionary and returns a work order list contains listings and their matching locks

  Parameters:
  ----------
  None

  Returns:
  ----------
  workOrderList: list
    List contains reservations and their check in/out dates listings and their matching locks
  """
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

def programCodes(workorder:list)->None:
  """
  Sends request to Wink API and program the asked locks with user codes 

  Parameters:
  ----------
  workorder: list
    List contains reservations and their check in/out dates listings and their matching locks

  Returns:
  ----------
  None
  """
  authToken = get_wink_secret()
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
                print("--------------------------------------------")
                print ("POST request for: ", guestName)
                print ("lock:", list(lock_name.keys())[list(lock_name.values()).index(lock)]) 
                print("--------------------------------------------")
                print ("url: ", url)
                print ("payload: ", payload)
                print("--------------------------------------------")
                print(f'DONE\n')

              except Exception as e:
                print(e)
        else: print ("No codes to program today")

def deleteCodes(workorder:list)->None:
  """
  Sends request to Wink API and delete the asked locks with user codes 

  Parameters:
  ----------
  workorder: list
    List contains reservations and their check in/out dates listings and their matching locks

  Returns:
  ----------
  None
  """
  authToken = get_wink_secret()
  if workorder==404:
      print ("No guest activity today")
  else:
    for guest in workorder:
      locks = guest['locks']
      for lock in locks:
        print(f'\n--------------------------------------------')
        print ("Lock:", lock,list(lock_name.keys())[list(lock_name.values()).index(lock)])  
        print("--------------------------------------------")
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
              print("--------------------------------------------")
              print ("Checking Out At: ", guestCheckOut)
              print ("lock:", list(lock_name.keys())[list(lock_name.values()).index(lock)]) 
              print("--------------------------------------------")
              print ("url: ", url)
              print ("payload: ", payload)
              print ("name: ",key['name'])
              print ("key_id: ", key['key_id'])
              print("--------------------------------------------")
              print(f'DONE\n')

            except Exception as e:
              print(e)
          else: print (key['name'], "Doesnt need to be deleted today")
        
def get_wink_secret()->None:
  """
  Retrieve a Wink connection token from AWS Secret Manager

  Parameters:
  ----------
  None

  Returns:
  ----------
  None
  """
  secret_name = "WinkKey"
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

def obtain_wink_token()->None:
  """
  Obtain a new connection token from Wink API and rotate it in AWS Secret Manager

  Parameters:
  ----------
  None

  Returns:
  ----------
  None
  """
  url = f'https://api.wink.com/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=refresh_token&refresh_token={refresh_token}'
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers)
  tokenResponseUtf8 = (response.text.encode('utf8'))
  jsonNewToken = json.loads(tokenResponseUtf8)
  newRefreshedToken = jsonNewToken['access_token']

  secret_name = "WinkKey"
  region_name = "us-east-2"
  # Create a Secrets Manager client
  session = boto3.session.Session()
  client = session.client(
      service_name='secretsmanager',
      region_name=region_name
  )
  put_secret_value_response = client.put_secret_value(
          SecretId=secret_name,
          SecretString = f'{{"authToken": \"Bearer {newRefreshedToken}\" }}'

  )
  print ("Access Token Has Been Refreshed")

# programCodes(makeWorkOrder())
# deleteCodes(makeWorkOrder())
# obtain_wink_token()
# print (get_wink_secret())