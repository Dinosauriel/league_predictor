import riot_api as api
from champions import champion_library
import numpy as np
import config as cfg
import os
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Concatenate, Dropout
from contextlib import redirect_stdout


champ_lib = champion_library()

def get_classifier():
	input_b1 = Input(name='b1_input', shape=(champ_lib.n))
	input_b2 = Input(name='b2_input', shape=(champ_lib.n))
	input_b3 = Input(name='b3_input', shape=(champ_lib.n))
	input_b4 = Input(name='b4_input', shape=(champ_lib.n))
	input_b5 = Input(name='b5_input', shape=(champ_lib.n))

	input_r1 = Input(name='r1_input', shape=(champ_lib.n))
	input_r2 = Input(name='r2_input', shape=(champ_lib.n))
	input_r3 = Input(name='r3_input', shape=(champ_lib.n))
	input_r4 = Input(name='r4_input', shape=(champ_lib.n))
	input_r5 = Input(name='r5_input', shape=(champ_lib.n))

	#break down input champion vectors into a dense "feature" vector
	champion_dense = Dense(10, activation='relu')

	#share weights of champion feature layer between all champions
	features_b1 = champion_dense(input_b1)
	features_b2 = champion_dense(input_b2)
	features_b3 = champion_dense(input_b3)
	features_b4 = champion_dense(input_b4)
	features_b5 = champion_dense(input_b5)

	features_r1 = champion_dense(input_r1)
	features_r2 = champion_dense(input_r2)
	features_r3 = champion_dense(input_r3)
	features_r4 = champion_dense(input_r4)
	features_r5 = champion_dense(input_r5)

	top_conc = Concatenate()([features_b1, features_r1])
	jgl_conc = Concatenate()([features_b2, features_r2])
	mid_conc = Concatenate()([features_b3, features_r3])
	adc_conc = Concatenate()([features_b4, features_r4])
	sup_conc = Concatenate()([features_b5, features_r5])

	top_matchup = Dense(8, activation='relu')(top_conc)
	jgl_matchup = Dense(8, activation='relu')(jgl_conc)
	mid_matchup = Dense(8, activation='relu')(mid_conc)
	adc_matchup = Dense(8, activation='relu')(adc_conc)
	sup_matchup = Dense(8, activation='relu')(sup_conc)

	team_b = Concatenate()([features_b1, features_b2, features_b3, features_b4, features_b5])
	team_r = Concatenate()([features_r1, features_r2, features_r3, features_r4, features_r5])

	team_b_dense = Dense(30, activation='relu')(team_b)
	team_r_dense = Dense(30, activation='relu')(team_r)

	game = Concatenate()([team_b_dense, team_r_dense, top_matchup, jgl_matchup, mid_matchup, adc_matchup, sup_matchup])
	out = Dense(1, activation='sigmoid')(game)

	classifier = Model(inputs=[input_b1, input_b2, input_b3, input_b4, input_b5, input_r1, input_r2, input_r3, input_r4, input_r5], outputs=out)

	classifier.compile(optimizer='Adam', loss='binary_crossentropy', metrics=['binary_accuracy'])

	return classifier

def output_model(model, name:str):
	if not os.path.isdir("model"):
		os.mkdir("model")

	with open("model/" + name + ".summary", "w") as f:
		with redirect_stdout(f):
			model.summary()

	tf.keras.utils.plot_model(model, to_file="model/" + name + ".png", show_shapes=True, dpi=200)
	model.save("model/" + name + ".weights")

def arrange_input(games):
	return {
		"b1_input": np.array([champ_lib.vector_from_champion_id(id) for id in games[:,2]]),
		"b2_input": np.array([champ_lib.vector_from_champion_id(id) for id in games[:,3]]),
		"b3_input": np.array([champ_lib.vector_from_champion_id(id) for id in games[:,4]]),
		"b4_input": np.array([champ_lib.vector_from_champion_id(id) for id in games[:,5]]),
		"b5_input": np.array([champ_lib.vector_from_champion_id(id) for id in games[:,6]]),
		"r1_input": np.array([champ_lib.vector_from_champion_id(id) for id in games[:,7]]),
		"r2_input": np.array([champ_lib.vector_from_champion_id(id) for id in games[:,8]]),
		"r3_input": np.array([champ_lib.vector_from_champion_id(id) for id in games[:,9]]),
		"r4_input": np.array([champ_lib.vector_from_champion_id(id) for id in games[:,10]]),
		"r5_input": np.array([champ_lib.vector_from_champion_id(id) for id in games[:,11]])
	}


print("reading games..")
games = np.genfromtxt("games.csv")
np.random.shuffle(games)

ids = games[:,0]
y = games[:,1]
X = arrange_input(games)

gpus = tf.config.experimental.list_physical_devices('GPU')
#print(gpus)
tf.config.experimental.set_memory_growth(gpus[0], True)

classifier = get_classifier()
classifier.fit(X, y, epochs=5, validation_split=0.05, batch_size=32)

output_model(classifier, "classifier")