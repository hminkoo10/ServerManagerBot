from flask import Flask,request,redirect,session
from threading import Thread
from random import randint
import os
import requests

app = Flask('')

API_ENDPOINT = "https://discord.com/api"
CLIENT_ID = 984982030104293476
CLIENT_SECRET = os.getenv("client_secret")
REDIRECT_URI = 'https://ServerManagerBot.hminkoo10.repl.co/callback/addtoguild'

def get_access_token(code):
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri' : REDIRECT_URI
        }
 
        access_token = requests.post(url="https://discord.com/api/oauth2/token", data=data).json()
        return access_token.get("access_token")
def get_user_json(access_token):
        url = f"{API_ENDPOINT}/users/@me"
        headers = {"Authorization": f"Bearer {access_token}"}
 
        user_object = requests.get(url=url, headers=headers).json()
        return user_object
def add_to_guild(access_token, userID):
        url = f"{API_ENDPOINT}/guilds/995259383493697650/members/{userID}"

        botToken = os.getenv("token")
        data = {
        "access_token" : access_token,
    }
        headers = {
        "Authorization" : f"Bot {botToken}",
        'Content-Type': 'application/json'

    }
        requests.put(url=url, headers=headers, json=data)
@app.route('/')
def home():
    return 'Im in!'
@app.route('/callback/addtoguild')
def callbackaddtoguild():
    code = request.args.get("code")
    code1 = get_access_token(code)
    user = get_user_json(code1)
    user_id = user.get("id")
    add_to_guild(code1, user_id)
    return redirect("https://discord.com/oauth2/authorized")
def run():
    app.run(host='0.0.0.0', port=randint(2000, 9000))


def keep_alive():
    t = Thread(target=run)
    t.start()
