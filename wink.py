import requests
# from secret.devices import locks
from bnb import getTodaysCheckins

TodaysCheckins = getTodaysCheckins()
print (TodaysCheckins)

def makeWorkOrder():
  print ("Work Order Is Ready")

def programLocks():
  print ("Boop Boop - Lock Has Been Programmed")