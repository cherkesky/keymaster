## For local running (authToken is not saved in AWS Secret Manager and saved in secret/bnb_keys.py instead)
# Replace the methods get_secret & obtain_token with the following code and refactor all the HTTP requests in the bnb.py file to get their authToken from bnb_keys.authToken instead.



def getRefreshedToken(fromGetTodaysCheckins=False):
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
  if fromGetTodaysCheckins==True:
    return getTodaysCheckins()