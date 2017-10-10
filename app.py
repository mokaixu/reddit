# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests

import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)  # name will be different if imported


def create_slack_msg(text, title, url, img_url):
    return {
        'text': text,
        'attachments': [
            {
                'title': title,
                'title_link': url,
                'thumb_url': img_url
            }
        ]
    }


def is_image(domain):
    return domain == 'i.redd.it'


def format_webhook_response(message, slack_message):
    return {'speech': message,
            'displayText': message,
            'data': {'slack': slack_message},
            'source': 'apiai-webhook'}


def get_posts_response(data):
    # get the data you ade in process req
    print(data)
    message = 'Here are the posts and Links.\n'
    posts = data['data']['children']
    for post in posts:
        post_data = post['data']
        url = post_data['url']
        title = post_data['title']
        message += title + '\n' + url + '\n'
        reddit_logo = 'http://goo.gl/iNmoqv'

    slack_message = create_slack_msg("Here are the posts and links!",
                                     title, url, reddit_logo)

    return format_webhook_response(message, slack_message)


# format the response sent back to API AI
def get_read_posts_response(data):
    main_post = data[0]['data']['children'][0]
    title = main_post['title']

    is_image_post = is_image['domain']
    if is_image_post:
        message = 'Here's more info about the post!'
        img_url = main_post['url']
        url = img_url

    else:
        title = main_post['title']
        message = main_post['selftext']
        url = main_post['url']
        img_url = 'http://goo.gl/iNmoqv'

    slack_message = create_slack_msg(message, title, url, img_url)

    return format_webhook_response(message, slack_message)


# make a call to external service to
# process data retrieved from API AI
def processReq(req):
    BASE_URL = 'http://reddit.com'
    action = req['result']['action']
    params = req['result']['parameters']
    num_posts = 5
    if action == '':
        return {}

    # if the user has specified interest in a subreddit
    # reply with the titles/urls of the sub
    # user can later input link to get more info
    if action == 'get_posts':
        subreddit = params['subreddit']
        users = params['users']
        query_params = params['query_params']
        num_posts = params['sys.number']

        if subreddit:
            URL = BASE_URL + '/r/' + subreddit

            if query_params:
                URL = URL + '/' + query_params + '/'

        URL += '.json?limit=' + num_posts

        try:
            result = requests.get(URL).text
            data = json.loads(result)
            res = get_posts_response(data)

        except requests.exceptions.ConnectionError as e:
            print(e)

        return res

    # if API AI has identified the user has submitted a link
    # reply with the contents of the link
    if action == 'read_posts':
        post_link = params['sys.url']
        if 'reddit.com' not in post_link:
            return {}

        URL = post_link + '.json'

        try:
            result = requests.get(URL).text
            data = json.loads(result)
            res = get_read_posts_response(data)

        except requests.exceptions.ConnectionError as e:
            print(e)

        return res

    else:
        return {}


# if API AI identifies any intents, will POST
# data to webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    resp = processReq(req)
    resp = json.dumps(resp)
    r = make_response(resp)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('starting app on port')
    app.run()
