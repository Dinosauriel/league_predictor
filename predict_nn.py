import tensorflow as tf
import numpy as np
from champions import champion_library

class Predictor():
	model: object
	championLibrary: champion_library

	def __init__(self) -> None:
		self.model = tf.keras.models.load_model("model/classifier.weights")
		self.championLibrary = champion_library()

	def predict(self, champion_ids):

		i = {
			"b1_input": np.array([self.championLibrary.vector_from_champion_id(champion_ids[0])]),
			"b2_input": np.array([self.championLibrary.vector_from_champion_id(champion_ids[1])]),
			"b3_input": np.array([self.championLibrary.vector_from_champion_id(champion_ids[2])]),
			"b4_input": np.array([self.championLibrary.vector_from_champion_id(champion_ids[3])]),
			"b5_input": np.array([self.championLibrary.vector_from_champion_id(champion_ids[4])]),
			"r1_input": np.array([self.championLibrary.vector_from_champion_id(champion_ids[5])]),
			"r2_input": np.array([self.championLibrary.vector_from_champion_id(champion_ids[6])]),
			"r3_input": np.array([self.championLibrary.vector_from_champion_id(champion_ids[7])]),
			"r4_input": np.array([self.championLibrary.vector_from_champion_id(champion_ids[8])]),
			"r5_input": np.array([self.championLibrary.vector_from_champion_id(champion_ids[9])])
		}

		return self.model.predict(i)[0][0]

if __name__ == "__main__":
	p = Predictor()
	prediction = p.predict([1,2,3,4,5,6,7,8,9,10])
	print(prediction)