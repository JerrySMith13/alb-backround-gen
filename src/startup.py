from flask import Flask, request, redirect
import requests
import base64
import os
import sys
import json

app = Flask(__name__)

CLIENT_ID = "63572a5aba3b43d49f9a4cac0d1f4dcb"
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIR_URI = "http://127.0.0.1:5000"

@app.route("/start")
def start():
    return redirect(f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIR_URI}&scope=user-top-read")


@app.route("/")
def redir():
    args = request.args
    code = args.get("code")
    err = args.get("error")
    if code == None:
        return "<p>Error: {err}</p>"
    url = f"https://accounts.spotify.com/api/token"
    msg = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_bytes = msg.encode('ascii')
    base64str = base64.b64encode(b64_bytes).decode('ascii')
    headers = {
                "content-type":"application/x-www-form-urlencoded",
                "authorization":f"Basic {base64str}"
            }
    body =f"grant_type=authorization_code&code={code}&redirect_uri={REDIR_URI}"
    response = requests.post(url, headers=headers, data=body)

    if response.status_code != 200:
        err = response.text
        return f"<p>Spotify error: {err}"

    with open("./.code", 'w') as file:
        file.write(response.text)
        return "<p>Success! you may now close this window</p>"
 
def refresh():
    f = open("./.code")
    data = json.load(f)
    token = data["refresh_token"]

    msg = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_bytes = msg.encode('ascii')
    base64str = base64.b64encode(b64_bytes).decode('ascii')

    url = "https://accounts.spotify.com/api/token"
    
    body = f"grant_type=refresh_token&refresh_token={token}"
    headers = {"content-type": "application/x-www-form-urlencoded",
               "authorization": f"Basic {base64str}"
               }
    response = requests.post(url, headers=headers, data=body)
    with open("./.code", 'w') as file:
        file.write(response.text)
        
    data = json.load(response.text)
    auth_token = data["access_token"]
    return auth_token



