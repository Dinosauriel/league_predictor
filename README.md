# League Predictor
Training a NN to predict my league of legends games :)

## Dependencies
### Required
- Python 3.8 with following modules
	- tensorflow
	- json
	- pickle
	- numpy
	- glob
	- os
	- pydot (for model plotting)
	- flask
- Graphviz (for model plotting) [https://graphviz.gitlab.io/download/]

### GPU Support (optional)
For GPU support, you will need to install the required GPU drivers, CUDA Toolkit etc. Refer to the following link for installation: [https://www.tensorflow.org/install/gpu]



## Instructions
The project is divided into several scripts:

### `config.py`
To get started, copy the file `config.example.py` to `config.py` . In `config.py` you will have to to change the values `api_key` and `root_summoner_name`. Depending on your region, you may also have to change `host`.

### `champions.py`
This is a supporting class that manages champions.

### `scrape_games.py`
This script uses the Riot API to search for games. It stores any scraped games as json in the folder `lake/`. In one execution, it scrapes as many games as defined in `config.games_per_scrape`. It keeps state in the folder `scrape_cache/`, so you can run the script multiple times without scraping duplicate games. To reset, just delete the files in `scrape_cache/`.

### `preprocess_games.py`
This script iterates through all the games in the folder `lake/` and extracts the relevant information for the neural net. It stores (appends) the output in `processed_games.csv`.

### `train_nn.py`
This script creates a new neural net and trains it using the games stored in `preprocessed_games.csv`. It stores the model itself in `model/classifier.weights/` and some metadata in `model/`.

### `predict_nn.py`
This script loads the neural net from `model/classifier.weights`.

### `web.py`
This script implements the webinterface using the flask [https://flask.palletsprojects.com] python module.
To start the server *for development*, use:
$bash:
```
export FLASK_APP=web.py
python -m flask run
```

PowerShell:
```
$env:FLASK_APP = "web.py"
python -m flask run
```