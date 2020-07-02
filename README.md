![Keymaster](https://github.com/cherkesky/keymaster/blob/master/keymaster_logo.png)

### by Guy Cherkesky | [LinkedIn](http://linkedin.com/in/cherkesky) | [Website](http://cherkesky.com)

Keymaster is a tool for Airbnb owners to streamline their guest's check-in/out procedure.
Every day at checkin time Keymaster reaches out to check if there are any guests coming in today, generates a custom user code based on the last 4 digits of the customer's phone number, and then reaches out to the property's smart hub with a request to program the locks. On check-out time the tool will delete the key codes from the locks (on the next update it can also set the smart thermostat to 'eco' mode as an option).


<img src="https://github.com/cherkesky/keymaster/blob/master/design.png" height="500" width="800">

## Flows
#### Program Codes: 
1. EventBridge triggers the keymasterFn lambda every day at 2:30PM
2. Authorization token is being retrieved from AWS Secret Manager
3. A GET request for this week's reservations is sent to the BNB API with the retrieved credentials
4. The bnb.py layer processes the response and build a workorder for the wink.py layer
5. The wink.py layer send a POST request to the Smart Hub API to program the locks with custom user codes for the guests that are checking in today
6. Logs from the CloudWatch are being stream to KeymasterLogsFn lambda 
7. KeymasterLogsFn lambda processes the log files and parses it to a HTML code
8. A customized email is being sent through AWS SES to system admin with a report containes the recent activity

#### Delete Codes: 
1. EventBridge triggers the keymasterFn lambda every day at 2:15PM
2. Authorization token is being retrieved from AWS Secret Manager
3. A GET request for this week's reservations is sent to the BNB API with the retrieved credentials
4. The bnb.py layer processes the response and build a workorder for the wink.py layer
5. The wink.py layer send a POST request to the Smart Hub API to delete the codes from the locks for the guests that checked out today
6. Logs from the CloudWatch are being stream to KeymasterLogsFn lambda 
7. KeymasterLogsFn lambda processes the log files and parses it to a HTML code
8. A customized email is being sent through AWS SES to system admin with a report containes the recent activity

#### Rotate Token: 
1. EventBridge triggers the keymasterFn lambda every 10 hours
2. Refresh token is being retrieved from AWS Secret Manager
3. A POST request is sent to the BNB API with the refresh token in order to obtain a new auth token
4. A request to update the old auth token with the new obtained one sent to AWS Secret Manager
