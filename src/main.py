from flask import Flask, request, redirect
import requests
import base64

app = Flask(__name__)

CLIENT_ID = "63572a5aba3b43d49f9a4cac0d1f4dcb"
CLIENT_SECRET = env.

@app.route("/start")
def start():
    return redirect(f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=http://127.0.0.1:5000&scope=user-top-read")


@app.route("/")
def redir():
    args = request.args
    code = args["code"]
    url = f"https://accounts.spotify.com/api/token?
            code={code}
            &grant_type=authorization_code
            &redirect_uri=127.0.0.1"
    base64str = base64.encode(f"")
    headers = {
                "content-type":"application/x-www-form-urlencoded",
                "Authorization":"Basi"
            }

