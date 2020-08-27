import numpy as np
import riot_api as api
import config as cfg

def extract_comp(match_info):
	game_id = match_info["gameId"]
	blue_wins = (match_info["teams"][0]["teamId"] == 100 and match_info["teams"][0]["win"] == "Win") or (match_info["teams"][0]["teamId"] == 200 and match_info["teams"][0]["win"] == " Fail")
	blue_wins = int(blue_wins)

	blue_champs = [x["championId"] for x in match_info["participants"] if x["teamId"] == 100]
	red_champs  = [x["championId"] for x in match_info["participants"] if x["teamId"] == 200]

	return np.concatenate(([game_id, blue_wins], blue_champs, red_champs))

def extract_account_ids(match_info):
	ids = [x["player"]["accountId"] for x in match_info["participantIdentities"]]
	return set(ids)

#number of games
N = 150
scraped_games = set()
visited_accounts = set()
X = np.empty((N, 12))

#perform "graph search"
next_account_ids = {api.getAccountId(cfg.root_summoner_name)}

while len(scraped_games) < N:

	account_id = next_account_ids.pop()
	
	#dont scrape an account twice
	if account_id in visited_accounts:
		continue

	visited_accounts.add(account_id)
	print("evaluating account no: " + str(len(visited_accounts)))


	match_history = api.getMatchHistory(account_id)
	print("fetched " + str(len(match_history)) + " most recent matches for account id " + account_id)

	for match in match_history:
		print("there are " + str(len(scraped_games)) + " scraped games, and " + str(len(next_account_ids)) + " next accounts")

		if len(scraped_games) >= N:
			break

		if match["gameId"] in scraped_games:
			continue

		match_info = api.getMatchInfo(match["gameId"])

		X[len(scraped_games)] = extract_comp(match_info)
		scraped_games.add(match["gameId"])

		new_account_ids = extract_account_ids(match_info).difference(visited_accounts)
		next_account_ids.update(new_account_ids)

np.savetxt("games.csv", X, fmt="%d")
