import glob
import json
import numpy as np
import config as cfg
import games

#returns True if the game should be preprocessed and added to the output
#returns False if the game should be skipped
def filter_game(game) -> bool:
	return len(game["participants"]) == 10 and games.patch_is_greater_or_equal(game["gameVersion"], cfg.preprocessor_min_patch)

def preprocess_game(game) -> np.array:
	game_id = game["gameId"]
	blue_wins = (game["teams"][0]["teamId"] == 100 and game["teams"][0]["win"] == "Win") or (game["teams"][0]["teamId"] == 200 and game["teams"][0]["win"] == " Fail")
	blue_wins = int(blue_wins)

	try:
		teams = games.extract_team_compositions(game)
	except:
		return None

	blue_champs = [x["championId"] for x in teams["blue"]]
	red_champs  = [x["championId"] for x in teams["red"]]

	return np.concatenate(([game_id, blue_wins], blue_champs, red_champs))

def preprocess_games():
	n_invalid_games = 0
	n_filtered_games = 0
	i = 0
	with open("games.csv", "a") as output_file:
		for game_json_path in glob.iglob("_lake/*.json", recursive=False):
			i += 1
			if i % 1000 == 0:
				print("preprocessing game " + str(i) + ": " + game_json_path)
			with open(game_json_path, "r") as game_json:
				game = json.load(game_json)
				if not filter_game(game):
					n_filtered_games
					continue
				processed = preprocess_game(game)
				if processed is None:
					n_invalid_games += 1
					continue

				np.savetxt(output_file, [processed], fmt="%d")
	print("total games:", i, ", invalid games:", n_invalid_games, ", filtered games:", n_filtered_games)
				

preprocess_games()