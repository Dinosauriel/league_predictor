import numpy as np
import riot_api as api
import config as cfg


NUMBER_OF_GAMES = 1000

account_id = api.getAccountId(cfg.root_summoner_name)
print("fetched account id: " + account_id)

match_history = api.getMatchHistory(account_id)
print("fetched " + str(len(match_history)) + " most recent matches for account id " + account_id)

#print(match_history[0])

match_history_ids = []
for match in match_history:
	match_history_ids.append(match['gameId'])

#print(match_history_ids)

def extract_comp(match_info):
	game_id = match_info["gameId"]
	blue_champs = []
	red_champs = []

	blue_wins = (match_info["teams"][0]["teamId"] == 100 and match_info["teams"][0]["win"] == "Win") or (match_info["teams"][0]["teamId"] == 200 and match_info["teams"][0]["win"] == " Fail")
	blue_wins = int(blue_wins)

	for participant in match_info["participants"]:
		if participant["teamId"] == 100:
			blue_champs.append(participant["championId"])
		else:
			red_champs.append(participant["championId"])

	return np.concatenate(([game_id, blue_wins], blue_champs, red_champs))

X = np.empty((100, 12))
for i, match_id in enumerate(match_history_ids):
	print("fetching match " + str(i))
	match_info = api.getMatchInfo(match_id)
	X[i] = extract_comp(match_info)

np.savetxt("games.csv", X, fmt="%d")

#print(match_info)