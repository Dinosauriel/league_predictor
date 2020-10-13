def extract_team_composition(team):
	composition = {}
	for participant in team:
		role = participant["timeline"]["role"]
		lane = participant["timeline"]["lane"]

		position = ""
		if lane == "JUNGLE":
			position = "jungle"
		elif lane == "MIDDLE" or lane == "MID":
			position = "mid"
		elif lane == "TOP":
			position = "top"
		elif lane == "BOTTOM" or lane == "BOT":
			if role == "DUO_CARRY" or "DUO":
				position = "bottom"
			elif role == "DUO_SUPPORT":
				position = "support"

		if position == "":
			raise Exception("could not assign a position for " + role + ", " + lane)

		if position in composition:
			raise Exception("found duplicate position")

		composition[position] = participant

	return composition


def extract_team_compositions(game):
	team_blue = [participant for participant in game["participants"] if participant["teamId"] == 100]
	team_red = [participant for participant in game["participants"] if participant["teamId"] == 200]

	assert len(team_blue) == 5 and len(team_red) == 5

	teams = {
		"blue": extract_team_composition(team_blue),
		"red": extract_team_composition(team_red)
	}

	return teams

def extract_champion_ids_from_active_game(active_game):
	team_blue = [participant["championId"] for participant in active_game["participants"] if participant["teamId"] == 100]
	team_red = [participant["championId"] for participant in active_game["participants"] if participant["teamId"] == 200]

	teams = {
		"blue": team_blue,
		"red": team_red
	}

	return teams