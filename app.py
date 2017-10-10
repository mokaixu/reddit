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

import requests

import json
import os


from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__) # name will be different if imported

def getWebhookRes(data):
	# get the data you ade in process req
	print(data)
	message = "Here are the posts and Links.\n"

	posts = data['data']['children'] #self_text
	for post in posts:
		post_data = post['data']
		url = post_data['url']
		title = post_data['title']
		message += title + '\n' + url + '\n'
		imgurl = "http://goo.gl/iNmoqv"


	slack_message = {
        "text": message,
        "attachments": [
            {
                "title": title,
                "title_link": url,
                "thumb_url": imgurl
            }
        ]
    }

	return {"speech": message, "displayText": message, "data": {"slack": slack_message}, "source": "apiai-webhook"}

def processReq(req):
	action = req['result']['action']
	params = req['result']['parameters']
	if action == "":
		return {}

	if action == "getPosts":
		subreddit = params["subreddit"]
		users = params["users"]
		query_params = params["query_params"]
		URL = "http://reddit.com"

		if subreddit:
			URL += "/r/" + subreddit
			
		URL += ".json?limit=1"

		if query_params:
			URL += "?sort=" + query_params

		result = requests.get(URL).text
		data = json.loads(result)
		res = getWebhookRes(data)

		#blah
	if action == "searchPhotos":
		thing_to_search = params['any']
		query_params = params['query_params']
		URL = "http://www.reddit.com/r/pics/search.json" + "?q=" + thing_to_search
		if query_params:
			URL = URL + "?sort=" + query_params;

		result = requests.get(URL).text
		data = json.loads(result)

	return res

@app.route('/hello', methods=['GET'])
def hello():
	res = {"hello": "hi"}
	r = json.dumps(res)
	r_obj = make_response(r)
	r_obj.headers['Content-Type'] = 'application/json'
	return r_obj

@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json()
	resp = processReq(req)
	resp = json.dumps(resp)
	   	#converts the return value from a view fc to ar eal response obj
	   	# returns a Response object
	r_obj = make_response(resp)
	r_obj.headers['Content-Type'] = 'application/json'
	return r_obj




if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print("starting app on port")
	app.run()
