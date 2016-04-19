#!/bin/bash

curl \
--include \
--header "Authorization: BC_TOKEN {ENTER TOKEN HERE}" \
--data 'name=NewApp03&maximum_scope=[{
"identity": {
"type": "video-cloud-account",
"account-id": "{BC ACCOUNT ID}"
},
"operations": [
"video-cloud/video/all",
"video-cloud/player/all",
"video-cloud/ingest-profiles/profile/read",
"video-cloud/ingest-profiles/account/read"
]
}]' \
https://oauth.brightcove.com/v3/client_credentials


