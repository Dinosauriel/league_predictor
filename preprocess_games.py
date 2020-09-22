import glob
import json
import numpy as np

#returns True if the game should be preprocessed and added to the output
#returns False if the game should be skipped
def filter_game(game) -> bool:
	return len(game["participants"]) == 10

def preprocess_game(game) -> np.array:
	game_id = game["gameId"]
	blue_wins = (game["teams"][0]["teamId"] == 100 and game["teams"][0]["win"] == "Win") or (game["teams"][0]["teamId"] == 200 and game["teams"][0]["win"] == " Fail")
	blue_wins = int(blue_wins)

	blue_champs = [x["championId"] for x in game["participants"] if x["teamId"] == 100]
	red_champs  = [x["championId"] for x in game["participants"] if x["teamId"] == 200]

	return np.concatenate(([game_id, blue_wins], blue_champs, red_champs))

def preprocess_games():
	i = 0
	with open("games.csv", "a") as output_file:
		for game_json_path in glob.iglob("lake/*.json", recursive=False):
			i += 1
			if i % 100 == 0:
				print("processing game " + str(i) + ": " + game_json_path)
			with open(game_json_path, "r") as game_json:
				game = json.load(game_json)
				if not filter_game(game):
					continue
				processed = preprocess_game(game)
				np.savetxt(output_file, [processed], fmt="%d")

preprocess_games()