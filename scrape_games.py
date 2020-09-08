import numpy as np
import riot_api as api
import config as cfg
import os.path
import pickle
import json

def extract_account_ids(match_info):
	ids = [x["player"]["accountId"] for x in match_info["participantIdentities"]]
	return set(ids)

def save_to_cache(cached_games, scraped_games, next_account_ids):
	print("saving " + str(len(scraped_games)) + " scraped games, " + str(len(cached_games)) + " cached games and " + str(len(next_account_ids)) + " next account ids to cache.")

	if not os.path.isdir("scrape_cache"):
		os.mkdir("scrape_cache")

	#save state to cache to continue where we left off last time
	with open("scrape_cache/scraped_game_ids", "wb") as f:
		pickle.dump(cached_games.union(scraped_games), f)
	with open("scrape_cache/next_account_ids", "wb") as f:
		pickle.dump(next_account_ids, f)


if not os.path.isdir("lake"):
	os.mkdir("lake")


#target number of games
N = cfg.games_per_scrape
print("scraping " + str(N) + " new games...")

scraped_games = set()
visited_accounts = set()

#load previously scraped games from cache if possible
cached_games = set()
if os.path.isfile("scrape_cache/scraped_game_ids"):
	with open("scrape_cache/scraped_game_ids", "rb") as f:
		cached_games = pickle.load(f)
		print("loading " + str(len(cached_games)) + " scraped game ids from cache")

next_account_ids = {api.getAccountId(cfg.root_summoner_name)}

#load next accounts from cache if possible
if os.path.isfile("scrape_cache/next_account_ids"):
	with open("scrape_cache/next_account_ids", "rb") as f:
		cached = pickle.load(f)
	print("loading " + str(len(cached)) + " next accound ids from cache")
	next_account_ids.update(cached)

#perform "graph search"

while len(scraped_games) < N:

	account_id = next_account_ids.pop()
	
	#dont scrape an account twice
	if account_id in visited_accounts:
		continue

	visited_accounts.add(account_id)
	print("evaluating account no: " + str(len(visited_accounts)))


	try:
		match_history = api.getMatchHistory(str(account_id))
	except Exception as e:
		print("could not fetch match history for account id " + str(account_id) + ". skipping...")
		continue

	print("fetched " + str(len(match_history)) + " most recent matches for account id " + str(account_id))

	for match in match_history:
		print("there are " + str(len(scraped_games)) + " newly scraped games and " + str(len(next_account_ids)) + " next accounts")

		if len(scraped_games) >= N:
			break

		if match["gameId"] in scraped_games or match["gameId"] in cached_games:
			print("game with id " + str(match["gameId"]) + " already scraped. skipping...")
			continue

		try:
			match_info = api.getMatchInfo(match["gameId"])
		except Exception as e:
			print("match fetch request failed... skipping...")
			continue

		with open("lake/" + str(match["gameId"]) + ".json", "w") as f:
			json.dump(match_info, f)

		scraped_games.add(match["gameId"])

		try:
			new_account_ids = extract_account_ids(match_info).difference(visited_accounts)
			next_account_ids.update(new_account_ids)
		except Exception as e:
			print("could not extract new accounts from game " + str(match["gameId"]))

		#backup every 10'000 games
		if len(scraped_games) % 10000 == 0:
			save_to_cache(cached_games, scraped_games, next_account_ids)

save_to_cache(cached_games, scraped_games, next_account_ids)
