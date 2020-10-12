from flask import Flask, request
from flask.helpers import send_file
from predict_nn import Predictor
import riot_api

app = Flask("league_predictor", static_folder="web/static")

pred = Predictor()

@app.route("/")
def index():
	return send_file("web/index.html")

@app.route("/active-game/<string:summoner_name>")
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

@app.route("/predict", methods=["POST"])
def predict_game():
	try:
		comp = [
			request.args.get("b1", type=int),
			request.args.get("b2", type=int),
			request.args.get("b3", type=int),
			request.args.get("b4", type=int),
			request.args.get("b5", type=int),
			request.args.get("r1", type=int),
			request.args.get("r2", type=int),
			request.args.get("r3", type=int),
			request.args.get("r4", type=int),
			request.args.get("r5", type=int)
		]
	except Exception as e:
		print(e)
		return "invalid url parameters", 400
	

	return { "prediction": float(pred.predict(comp)) }