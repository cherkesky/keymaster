import requests
from secret.devices import listinglocks
from bnb import getTodaysCheckins

TodaysCheckins = getTodaysCheckins()

def makeWorkOrder():
  workOrderDict={}
  for checkin in TodaysCheckins:
    workOrderDict['name'] = checkin['name']
    workOrderDict['code'] = checkin['code']
    workOrderDict['checkin'] = checkin['checkin']
    workOrderDict['checkout'] = checkin['checkout']
    workOrderDict['locks']= listinglocks[checkin['listing']]
  return workOrderDict
    
def programCodes():
  print ("Boop Boop - Codes Has Been Programmed")

def deleteCodes():
  print ("Boop Boop - Codes Has Been Deleted")


print (makeWorkOrder())