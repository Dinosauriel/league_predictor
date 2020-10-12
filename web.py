from flask import Flask
from flask.helpers import send_file
import riot_api

app = Flask("league_predictor", static_folder="web/static")

@app.route("/")
def index():
	return send_file("web/index.html")

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

	return active_game_info