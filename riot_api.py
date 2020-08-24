import config as cfg
import requests
import json

HOST = "https://" + cfg.host
HEADERS = {"X-Riot-Token": cfg.api_key}

#path: resource without hostname
def get(path: str, parameters: dict={}):
	r = requests.get(HOST + path, headers=HEADERS, params=parameters)
	return json.loads(r.text)


def getAccountId(summoner_name: str):
	return get("/lol/summoner/v4/summoners/by-name/" + summoner_name)["accountId"]

def getMatchHistory(account_id: str):
	return get("/lol/match/v4/matchlists/by-account/" + account_id)["matches"]