![Keymaster](https://github.com/cherkesky/keymaster/blob/master/keymaster_logo.png)

### by Guy Cherkesky | [LinkedIn](http://linkedin.com/in/cherkesky) | [Website](http://cherkesky.com)

Keymaster is a tool for Airbnb owners to streamline their guests' check-in/out procedure.
Every day at check-in time Keymaster reaches out to check if there are any guests coming in today, generates a custom user code based on the last 4 digits of the customer's phone number, and then reaches out to the property's smart hub with a request to program the locks. On check-out time the tool will delete the key codes from the locks (on the next update it will also set the smart thermostats to 'eco' mode upon checkout).


Introduced  at NashJS July 2020 Monthly Meeting: https://bit.ly/KeymasterLive

### Update
#### The app changed it name to Maistr and grew beyond this codebase to a private repository. The app provides free of charge code management systems to selected Airbnb owners in Nashville, TN.
#### Updated Architecture + Design: 
<img src="https://github.com/cherkesky/checkbnbavail/blob/main/arch.jpeg" height="500" width="800">

#### Original Design: 
<img src="https://github.com/cherkesky/keymaster/blob/master/design.png" height="500" width="800">

#### KeymasterFn lambda:
<img src="https://github.com/cherkesky/keymaster/blob/master/eventbridge.png" height="500" width="800">

#### Sample Report: 
<img src="https://github.com/cherkesky/keymaster/blob/master/report.png" height="500" width="800">


## Details

### Flows:

#### Program Codes: 
1. EventBridge triggers the keymasterFn lambda every day at 2:30PM
2. Authorization token is retrieved from AWS Secret Manager
3. A GET request for this week's reservations is sent to the BNB API with the retrieved credentials
4. The bnb.py layer processes the response and builds a workorder for the wink.py layer
5. The wink.py layer sends a POST request to the Smart Hub API to program the locks with custom user codes for today's guests
6. Logs from the CloudWatch are streamed to KeymasterLogsFn lambda 
7. KeymasterLogsFn lambda processes the log files and parses them to an HTML code using regex
8. A customized email is sent through AWS SES to the system admin with a report containing the recent activity

#### Delete Codes: 
1. EventBridge triggers the keymasterFn lambda every day at 2:15PM
2. Authorization token is retrieved from AWS Secret Manager
3. A GET request for this week's reservations is sent to the BNB API with the retrieved credentials
4. The bnb.py layer processes the response and builds a workorder for the wink.py layer
5. The wink.py layer sends a POST request to the Smart Hub API to delete the checked out guests' codes from the locks
6. Logs from the CloudWatch are streamed to KeymasterLogsFn lambda 
7. KeymasterLogsFn lambda processes the log files and parses them to an HTML code using regex
8. A customized email is sent through AWS SES to the system admin with a report containing the recent activity

#### Rotate Token: 
1. EventBridge triggers the keymasterFn lambda every 10 hours
2. Refresh token is retrieved from AWS Secret Manager
3. A POST request is sent to the BNB API with the refresh token in order to obtain a new auth token
4. A request to update the old auth token with the newly obtained one is sent to AWS Secret Manager


### Technology Stack: 
- Python
- AWS Roles: Custom IAM Roles (JSON)
- Email: AWS SES (Cross region integration)
- Lambda: Lambda Function, Python 3.8 Layers
- Cron: EventBridge using custom cron expressions
- Credentials: AWS Secret Manager, Static key files
- Logs: CloudWatch
- Version Control: Git, GitHub

The code for the KeymasterFn lambda:
https://gist.github.com/cherkesky/e77d6d1fd53e5c2af5d9bdb5ccc8b377

The code for the KeymasterLogsFn lambda:
https://gist.github.com/cherkesky/9f772b14fb5d454bc7532985891b83a3

