import config as cfg
import requests
import json
import time

HOST = "https://" + cfg.host
HEADERS = {"X-Riot-Token": cfg.api_key}

def get_raw(url: str, headers={}, parameters: dict={}):
	r = requests.get(url, headers=headers, params=parameters)
	print(r.url)
	#raise an error if response is not ok
	r.raise_for_status()
	return json.loads(r.text)

#path: resource without hostname
def get(path: str, parameters: dict={}):
	#rate limiting
	time.sleep(max([120.0/cfg.requests_per_2_minutes, 1.0/cfg.requests_per_sec]))
	return get_raw(HOST + path, headers=HEADERS, parameters=parameters)


def getAccountId(summoner_name: str):
	return get("/lol/summoner/v4/summoners/by-name/" + summoner_name)["accountId"]

def getSummonerId(summoner_name: str):
	return get("/lol/summoner/v4/summoners/by-name/" + summoner_name)["id"]

def getActiveGame(summoner_id: str):
	return get("/lol/spectator/v4/active-games/by-summoner/" + summoner_id)

def getMatchHistory(account_id: str):
	return get("/lol/match/v4/matchlists/by-account/" + account_id, parameters={'queue': cfg.queue_ids})["matches"]

def getMatchInfo(match_id: int):
	return get("/lol/match/v4/matches/" + str(match_id))