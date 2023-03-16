# Picbooth

Small App base on PyQt5 for a Photo Booth at a friend party, that can save the picture directly to a Google Drive
(using gcloud Python sdk) and send the picture to a Facebook Messenger conversation (using selenium as there is no 
API to do so in private conversations).


Env variables to fill:
```bash
FB_EMAIL=
FB_PASSWORD=
FB_CONVERSATION_ID=

DRIVE_FOLDER_ID=
SERVICE_ACCOUNT_KEY_PATH=./google-service-account-key.json
```
