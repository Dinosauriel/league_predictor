var config = {
	api: {
		urls: {
			static: {
				allChampions: "https://ddragon.leagueoflegends.com/cdn/10.20.1/data/en_US/champion.json",
				singleChampion: "http://ddragon.leagueoflegends.com/cdn/10.20.1/img/champion/"
			},
			dynamic: {
				activeGame: "/active-game/",
				predict: "/predict"
			}
		}
	}
}

const championSearchCard = {
	props: ['champion'],
	emits: ['champion-selected'],
	template: `
		<button class="dropdown-item" type="button" @click="$emit( 'champion-selected')">{{ champion.name }}</button>
	`
}

const championcard = {
	data: function() { return {
		championSearchTerm: ""
	}},
	components: {
		"champion-search-card": championSearchCard
	},
	props: ['id', 'player', 'champions'],
	computed: {
		champion: function() {
			return this.champions[this.player.championId]
		},
		imageUrl: function() {
			if (this.championIsSelected) {
				return config.api.urls.static.singleChampion + this.champion.image.full
			}
			return ""
		},
		buttonId: function() {
			return this.id + "-select-champion-button"
		},
		championSearchResults() {
			let results = {}
			for (var key in this.champions) {
				if (this.champions[key].name.toLowerCase().includes(this.championSearchTerm.toLowerCase())) {
					results[key] = this.champions[key]
				}
			}
			return results
		},
		championIsSelected() {
			return this.player.championId != -1
		},
	},
	mounted() {
		$("#" + this.id + " .dropdown").on("shown.bs.dropdown", this.selectSearchField)
	},
	methods: {
		selectSearchField(event) {
			$("#" + this.id + " input").select()
		}
	},
	template:
		`<div :id="id" class="card mt-2 mb-2">
		<div class="card-body">
			<div class="media">
				<img :src="imageUrl" class="mr-3 w-25">
				<div class="media-body">
					<h5 class="card-title">{{ championIsSelected ? champion.name : "no champion" }}</h5>
					<h6 class="card-subtitle mb-2 text-muted">{{ player.positionName }}</h6>
					<div class="dropdown">
						<button type="button" class="btn btn-outline-secondary dropdown-toggle" :id="buttonId" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							Change
						</button>
						<div class="dropdown-menu" :aria-labelledby="buttonId">
							<form>
								<input v-model="championSearchTerm" class="form-control" type="text" placeholder="Search">
							</form>
							<div class="dropdown-divider"></div>
							<div class="overflow-auto" style="max-height: 400px">
								<champion-search-card @champion-selected="player.championId = c.key" :key="c.id" v-for="c in championSearchResults" :champion="c"></champion-search-card>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>`
}

var app = new Vue({
	el: "#app",
	components: {
		"champion-card": championcard
	},
	data: {
		summonerName: "",
		isLoadingActiveGame: false,
		loadingActiveGameFailed: false,
		championsAreLoaded: false,
		prediction: undefined,
		allChampions: {},
		composition: {
			blue: {
				top: {
					positionName: "Top",
					championId: -1
				},
				jgl: {
					positionName: "Jungle",
					championId: -1
				},
				mid: {
					positionName: "Mid",
					championId: -1
				},
				bot: {
					positionName: "Bottom",
					championId: -1
				},
				sup: {
					positionName: "Support",
					championId: -1
				}
			},
			red: {
				top: {
					positionName: "Top",
					championId: -1
				},
				jgl: {
					positionName: "Jungle",
					championId: -1
				},
				mid: {
					positionName: "Mid",
					championId: -1
				},
				bot: {
					positionName: "Bottom",
					championId: -1
				},
				sup: {
					positionName: "Support",
					championId: -1
				}
			}
		}
	},
	created: function() {
		this.loadAllChampions()
		//this.loadActiveGameData()
	},
	methods: {
		loadAllChampions: function() {
			var v = this

			axios.get(config.api.urls.static.allChampions)
				.then(function (response) {
					for (var [key, value] of Object.entries(response.data.data)) {
						v.allChampions[value.key] = value
					}
					v.championsAreLoaded = true
					console.log("loaded all champions")
				})
				.catch(function (error) {
					console.error("error loading all champions " + error)
				})
		},
		loadActiveGameData: function(event) {
			event.preventDefault()
			var v = this
			v.isLoadingActiveGame = true

			axios.get(config.api.urls.dynamic.activeGame + v.summonerName)
				.then(function (response) {
					console.log("loaded active game data")
					if (response.data.blue[0] != undefined) {
						v.composition.blue.top.championId = response.data.blue[0]
					}
					if (response.data.blue[1] != undefined) {
						v.composition.blue.jgl.championId = response.data.blue[1]
					}
					if (response.data.blue[2] != undefined) {
						v.composition.blue.mid.championId = response.data.blue[2]
					}
					if (response.data.blue[3] != undefined) {
						v.composition.blue.bot.championId = response.data.blue[3]
					}
					if (response.data.blue[4] != undefined) {
						v.composition.blue.sup.championId = response.data.blue[4]
					}
					if (response.data.red[0] != undefined) {
						v.composition.red.top.championId = response.data.red[0]
					}
					if (response.data.red[1] != undefined) {
						v.composition.red.jgl.championId = response.data.red[1]
					}
					if (response.data.red[2] != undefined) {
						v.composition.red.mid.championId = response.data.red[2]
					}
					if (response.data.red[3] != undefined) {
						v.composition.red.bot.championId = response.data.red[3]
					}
					if (response.data.red[4] != undefined) {
						v.composition.red.sup.championId = response.data.red[4]
					}

					v.isLoadingActiveGame = false
					v.loadingActiveGameFailed = false
				})
				.catch(function (error) {
					v.isLoadingActiveGame = false
					v.loadingActiveGameFailed = true
				})
		},
		loadPrediction: function() {
			this.prediction = undefined
	
			var compositionVector = {
				"b1": this.composition.blue.top.championId,
				"b2": this.composition.blue.jgl.championId,
				"b3": this.composition.blue.mid.championId,
				"b4": this.composition.blue.bot.championId,
				"b5": this.composition.blue.sup.championId,
				"r1": this.composition.red.top.championId,
				"r2": this.composition.red.jgl.championId,
				"r3": this.composition.red.mid.championId,
				"r4": this.composition.red.bot.championId,
				"r5": this.composition.red.sup.championId,
			}
	
			for (var [key, id] of Object.entries(compositionVector)) {
				if (id == -1 || typeof id == "undefined") {
					return
				}
			}
	
			var v = this
	
			axios.post(config.api.urls.dynamic.predict, null, { params: compositionVector })
				.then(function (response) {
					v.prediction = response.data.prediction
				})
				.catch(function(error) {
					console.error("error loading prediction " + error)
				})
		}
	},
	computed: {
		isEven: function() {
			if (this.prediction == undefined) {
				return undefined
			}
			return this.prediction == 0.5
		},
		blueWins: function() {
			if (this.prediction == undefined) {
				return undefined
			}
			return this.prediction > 0.5
		},
		redWinds: function() {
			if (this.prediction == undefined) {
				return undefined
			}
			return this.prediction > 0.5
		},
		predictionPercentage: function() {
			return (Math.round(this.prediction * 10000) / 100) + "%"
		}
	},
	watch: {
		composition: {
			handler: function(newComp, oldComp) {
				this.loadPrediction()
			},
			deep: true
		}
	}
})