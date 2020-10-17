def patch_is_greater_than(a: str, b: str):
	"""
	Returns true if patch a is 'higher' than b

	2.0, 1.9 -> true
	"""
	al = a.split(".")
	bl = b.split(".")

	for i in range(min(len(al), len(bl))):
		if int(al[i]) > int(bl[i]):
			return True
		if int(al[i]) < int(bl[i]):
			return False

	return False

def patch_is_equal(a: str, b: str):
	"""
	Returns true if patch a is 'equal' to b

	2.0.2, 2.0 -> true
	"""
	al = a.split(".")
	bl = b.split(".")

	for i in range(min(len(al), len(bl))):
		if int(al[i]) != int(bl[i]):
			return False

	return True

def patch_is_greater_or_equal(a: str, b: str):
	return patch_is_greater_than(a, b) or patch_is_equal(a, b)

def extract_team_composition(team):
	#t = [(p["timeline"]["role"], p["timeline"]["lane"]) for p in team]


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
			if role == "DUO_CARRY" or role == "DUO":
				position = "bottom"
			elif role == "DUO_SUPPORT":
				position = "support"

		if position == "":
			raise Exception("could not assign a position for " + role + ", " + lane)

		if position in composition:
			raise Exception("found duplicate position " + position)

		composition[position] = participant

	return [composition["top"], composition["jungle"], composition["mid"], composition["bottom"], composition["support"]]


def extract_team_compositions(game):
	team_blue = [participant for participant in game["participants"] if participant["teamId"] == 100]
	team_red  = [participant for participant in game["participants"] if participant["teamId"] == 200]

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