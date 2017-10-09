# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__) # name will be different if imported

@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json()
	resp = processReq(req)
	resp = json.dumps(resp)
	   	#converts the return value from a view fc to ar eal response obj
	   	# returns a Response object
	r_obj = make_response(resp)
	r_obj.headers['Content-Type'] = 'application/json'
	return r

def proccessReq(req):
	action = req['result']['action']
	params = req['result']['parameters']

	if action == "searchReddit":

		#blah
	if action == "submitPost":
	#blah

	else:
		return {}


def getWebhookRes(data):
	# get the data you ade in process req
	item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
	reply = "Just submitted a post to"

	slack_message = {
        "text": reply,
        "attachments": [
            {
                "title": channel.get('title'),
                "title_link": channel.get('link'),
                "color": "#36a64f",

                "fields": [
                    {
                        "title": "Condition",
                        "value": "Temp " + condition.get('temp') +
                                 " " + units.get('temperature'),
                        "short": "false"
                    },
                    {
                        "title": "Wind",
                        "value": "Speed: " + channel.get('wind').get('speed') +
                                 ", direction: " + channel.get('wind').get('direction'),
                        "short": "true"
                    },
                    {
                        "title": "Atmosphere",
                        "value": "Humidity " + channel.get('atmosphere').get('humidity') +
                                 " pressure " + channel.get('atmosphere').get('pressure'),
                        "short": "true"
                    }
                ],

                "thumb_url": "http://l.yimg.com/a/i/us/we/52/" + condition.get('code') + ".gif"
            }
        ]
    }

    return {
    	"speech": reply,
    	"displayText": speech,
    	"data": {"slack": slack_message},
    	"source": "apiai-webhook"
    }

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5858))
	print "starting app on port %d" % port
	app.run()
