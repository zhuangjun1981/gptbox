import os
import requests
import json
import time
from dotenv import load_dotenv, set_key


def get_wx_token():
    curr_path = os.path.dirname(os.path.realpath(__file__))
    env_path = os.path.join(os.path.dirname(curr_path), ".env")
    load_dotenv()

    valid_time = os.getenv("WX_TOKEN_VALID_TIME")
    if valid_time and time.time() < int(valid_time):
        token = os.getenv("WX_ACCESS_TOKEN")
    else:
        appid = os.getenv("WX_APP_ID")
        secret = os.getenv("WX_APP_SECRET")

        wx_res = requests.get(
            f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
        )

        obj = json.loads(wx_res.content)
        token = obj["access_token"]
        valid_time = time.time() + obj["expires_in"] - 10
        set_key(env_path, "WX_ACCESS_TOKEN", token)
        set_key(env_path, "WX_TOKEN_VALID_TIME", str(int(valid_time)))

    return token
