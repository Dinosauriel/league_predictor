import riot_api as api
import config as cfg


account_id = api.getAccountId(cfg.root_summoner_name)
print("fetched account id: " + account_id)

match_history = api.getMatchHistory(account_id)
print("fetched " + str(len(match_history)) + " most recent matches for account id " + account_id)

match_history_ids = []
for match in match_history:
	match_history_ids.append(match['gameId'])

print(match_history_ids)