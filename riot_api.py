import config as cfg
import requests
import json

HOST = "https://" + cfg.host
HEADERS = {"X-Riot-Token": cfg.api_key}

#path: resource without hostname
def get(path: str, parameters: dict={}):
	r = requests.get(HOST + path, headers=HEADERS, params=parameters)
	#raise an error if response is not ok
	r.raise_for_status()
	return json.loads(r.text)

def get_raw(url: str):
	r = requests.get(url)
	#raise an error if response is not ok
	r.raise_for_status()
	return json.loads(r.text)


def getAccountId(summoner_name: str):
	return get("/lol/summoner/v4/summoners/by-name/" + summoner_name)["accountId"]

def getMatchHistory(account_id: str):
	return get("/lol/match/v4/matchlists/by-account/" + account_id, {'queue': cfg.queue_ids})["matches"]

def getMatchInfo(match_id: int):
	return get("/lol/match/v4/matches/" + str(match_id))

def getChampionLists():
	champs = get_raw(cfg.champions_json_url)["data"]

	#print(champs)

	ids = []
	names = []
	for key in champs:
		champ = champs[key]
		ids.append(int(champ["key"]))
		names.append(champ["name"])

	return (ids, names)
