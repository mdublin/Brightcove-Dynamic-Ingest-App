#! /usr/bin/python
# -*- coding: utf-8 -*-

#This is a JSON parser version of our script. Sometimes you can change a feed from JSON to MRSS by changing a parameter in the URL from JSON to MRSS. But just in case...

import BC_01
import json
import requests


r = requests.get('[Insert your JSON feed URL here]')
json = json.loads(r.text)
response_array = []

#counter = 0

for index, item in enumerate(json['items']):
    if index <= 2:
        print item['name']
        print item['id']
        #print item['FLVURL']
        print item['tags']
        print item['shortDescription']
        #print item['adKeys']
        renditions = item['renditions']
        max_url = None
        max_bitrate = 0
	    
#So since we're dealing with a dictionary
#we can get the nested "renditions" by saying item['renditions']		
#renditions itself is a list of dictionaries, so we say for each
#dictionary (which we call rend) in the rendition list
#check if its encodingRate (ie bitrate) is larger than the
#biggest bitrate we've seen so far in the renditions list
#if it is, assign the max_url and max_bitrate variables for the
#current rendition's url and encodingRate
#note that we set max_bitrate = 0 on line 27 so that means for each
#item in the feed we find the maximum bitrate for that item's rendition list

        for rend in renditions:
            if rend['encodingRate'] > max_bitrate:
                max_url = rend['url']
                max_bitrate = rend['encodingRate']
        print "MAX url", max_url, max_bitrate
        #counter += 1
      
        vid_url = max_url
        item['url'] = vid_url
        item['bit_rate'] = max_bitrate
    
        response_array.append(item)

refactored = []
for entity in response_array:
    new_el = entity
    new_el["name"] = entity["name"]
    new_el["description"] = entity["shortDescription"]
    del new_el["bit_rate"]

    refactored.append(new_el)
#print json.dumps(response_array, indent=4)

for idx,item in enumerate(refactored):
    if idx <= 2:
        name, url = item['name'], item['url']
        tags = item["tags"] if "tags" in item else []
        desc = item["description"] if "description" in item else ""
        if not BC_01.videoNameExists(name):
            print "did not see", name, "in brightcove, ingesting..."
            print "working on", name, url
            BC_01.createAndIngest(name, url, tags=tags, description=desc)
        else:
            print "already saw", name, "skipping..."

