from flask import Flask
import riot_api
import json

app = Flask("league_predictor")

@app.route("/")
def index():
	return "Hi"

@app.route("/active-game/<summoner_name>")
def active_game(summoner_name):
	try:
		encrypted_summoner_id = riot_api.getSummonerId(summoner_name)
	except Exception as e:
		print(e)
		return "summoner name not found", 404

	try:
		active_game_info = riot_api.getActiveGame(encrypted_summoner_id)
	except Exception as e:
		print(e)
		return "no active game found", 404

	return json.dumps(active_game_info)