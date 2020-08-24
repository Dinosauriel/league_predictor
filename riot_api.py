import config as cfg
import requests
import json

HOST = "https://" + cfg.host
HEADERS = {"X-Riot-Token": cfg.api_key}

#path: resource without hostname
def get(path: str):
	r = requests.get(HOST + path, headers=HEADERS)
	return json.loads(r.text)


def getAccountId(summoner_name: str):
	return get("/lol/summoner/v4/summoners/by-name/" + summoner_name)["accountId"]
