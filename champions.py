import config as cfg
import riot_api as api
import numpy as np

class champion_library:
	all: object
	ids: list
	names: list
	n: int

	def load(self):
		self.all = api.get_raw(cfg.champions_json_url)["data"].values()
		self.ids = [int(x["key"]) for x in self.all]
		self.names = [x["id"] for x in self.all]
		self.n = len(self.all)

	def vector_from_champion_id(self, id: int):
		if not id in self.ids:
			raise Exception("invalid champion id: " + str(id))

		v = np.zeros(self.n)
		v[self.ids.index(id)] = 1
		return v

	def __init__(self):
		self.load()