import glob
import json
import numpy as np
import config as cfg
import concurrent.futures
import time


def merge_stats(stats):
	stats = {
		"numberOfGames": sum([s["numberOfGames"] for s in stats]),
		"numberOfCustomGames": sum([s["numberOfCustomGames"] for s in stats]),
		"numberOfTutorialGames": sum([s["numberOfTutorialGames"] for s in stats]),
		"numberOfMatchedGames": sum([s["numberOfMatchedGames"] for s in stats])
	}

	return stats


def get_stats(games_json_paths):

	number_of_games = 0
	number_of_custom_games = 0
	number_of_tutorial_games = 0
	number_of_matched_games = 0

	number_of_games = 0
	for game_json_path in games_json_paths:
		number_of_games += 1
		if number_of_games % 1000 == 0:
			print("analyzing game " + str(number_of_games) + ": " + game_json_path)

		with open(game_json_path, "r") as game_json:
			game = json.load(game_json)


			if game["gameType"] == "CUSTOM_GAME":
				number_of_custom_games += 1
			elif game["gameType"] == "TUTORIAL_GAME":
				number_of_tutorial_games += 1
			elif game["gameType"] == "MATCHED_GAME":
				number_of_matched_games += 1

	stats = {
		"numberOfGames": number_of_games,
		"numberOfCustomGames": number_of_custom_games,
		"numberOfTutorialGames": number_of_tutorial_games,
		"numberOfMatchedGames": number_of_matched_games
	}

	return stats

def main():
	all_games = glob.glob("lake/*.json", recursive=False)

	t = cfg.number_of_threads
	n = len(all_games)
	b = n // t

	print("analyzing " + str(n) + " games on " + str(t) + " threads")

	executor = concurrent.futures.ThreadPoolExecutor(t)
	futures = []

	start = time.time()

	for thread_id in range(0, cfg.number_of_threads):
		if thread_id < cfg.number_of_threads:
			batch = all_games[b * thread_id : b * (thread_id + 1)]
		else:
			batch = all_games[b * thread_id :]

		future = executor.submit(get_stats, batch)
		futures.append(future)

	completed_futures = concurrent.futures.as_completed(futures)

	results = [f.result() for f in completed_futures]
	stats = merge_stats(results)

	end = time.time()
	print("took " + str(end - start) + " seconds")

	with open("stats.json", "w") as f:
		json.dump(stats, f)


main()