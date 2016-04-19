#! /usr/bin/python
# -*- coding: utf-8 -*-

#This is our Brightcove "module" containing both our oAuth procedure and the functions necessary for working with Brightcove's
#Dynamic Ingest API

print "Content-type: application/json\n\n"

import httplib
import urllib
import base64
import json
import requests
import models

#create video table object:
Video = models.Video()



#Read the oauth secrets and account ID from our oauth configuration file "brightcove_oauth.txt" located in 
#same directory as our Python scripts 

def loadSecret():
    credsFile=open('brightcove_oauth.json')
    creds = json.load(credsFile)
    return creds


# get the oauth 2.0 token
def getAuthToken(creds):
    conn = httplib.HTTPSConnection("oauth.brightcove.com")
    url =  "/v3/access_token"
    params = {
        "grant_type": "client_credentials"
    }
    client = creds["client_id"];
    client_secret = creds["client_secret"];
    authString = base64.encodestring('%s:%s' % (client, client_secret)).replace('\n', '')
    requestUrl = url + "?" + urllib.urlencode(params)
    headersMap = {
        "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + authString
    };
    conn.request("POST", requestUrl, headers=headersMap)
    response = conn.getresponse()
    if response.status == 200:
        data = response.read()
        result = json.loads( data )
        return result["access_token"]

    
#What follows below are three functions that tackle the multi-step Dynamic Ingest process. For more
#information on Brightcove's Dynamic Ingest API, see here: http://docs.brightcove.com/en/video-cloud/di-api/index.html

def createVid(account, token, name, tags=[], description=""):
    url = 'https://cms.api.brightcove.com/v1/accounts/{}/videos/'.format(account)
    headers = { "Authorization": "Bearer " + token, "Content-Type": "application/json" }
    data = {"name": name}
    if tags:
      data["tags"] = tags
    if description:
      data["description"] = description
    r = requests.post(url, data=json.dumps(data), headers=headers)
    res = json.loads(r.text)
    if "id" in res:
        vId = res['id']
        return vId


def ingestVid(account, token, vidId, videoUrl, profile="balanced-high-definition"):
    url = 'https://cms.api.brightcove.com/v1/accounts/[Insert Account ID]/videos/{}/ingest-requests'.format(vidId)
    headers = { "Authorization": "Bearer " + token, "Content-Type": "application/json" }
    data = {"master": {"url" : videoUrl}, "profile": profile}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    res = json.loads(r.text)
    return res


def createAndIngest(name, vUrl, tags=[], description=""):
    creds = loadSecret()
    token = getAuthToken(creds)
    account = creds["account_id"]
    vId = createVid(account, token, name, tags, description)
    print vId
    print "ingest"
    print ingestVid(account, token, vId, vUrl)
    return vId


#There's a bug with Brightcove's search_videos API call in that anytime we tried to search a video name with
#a colon in the title, brightcove would not list any search results so we would assume it was not found.
#To fix it, we replace any colons passed to the brightcove search endpoint with empty space. The problem
#has to do with how the video title is transformed when it's put into HTTP format, so when the title is passed
#to the BC API, video titles with a colon in them weren't being seen. That's why we're using the string repalce
#method in the videoNameExists function.

def videoNameExists(vidName):
    vidName = vidName.encode("utf-8")
    bugFixVidName = vidName.replace(":", "")
    search_url ='https://api.brightcove.com/services/library?command=search_videos&video_fields=name&page_number=0&get_item_count=true&token=[Insert API read token here]&any=%22{}%22'.format(bugFixVidName)

    r = requests.get(search_url)
    data = r.text
    result = json.loads(data)
    ans = result and not "error" in result and ("items" in result) and len(result["items"])
    if ans: # make sure we have an EXACT match
        items = result["items"]
        for item in items: # -- go through the results
            name = item["name"].encode("utf-8")
            if name == vidName: # -- does this name equal our original parameter?
                return True
    return False
