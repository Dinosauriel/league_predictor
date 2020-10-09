var config = {
	api: {
		urls: {
			static: {
				allChampions: "https://ddragon.leagueoflegends.com/cdn/10.20.1/data/en_US/champion.json",
				singleChampion: "http://ddragon.leagueoflegends.com/cdn/10.20.1/img/champion/"
			},
			dynamic: {
				activeGame: "/active-game/"
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
			return config.api.urls.static.singleChampion + this.champion.image.full
		},
		buttonId: function() {
			return this.id + "-select-champion-button"
		},
		championSearchResults() {
			let results = {}
			for (key in this.champions) {
				if (this.champions[key].name.toLowerCase().includes(this.championSearchTerm.toLowerCase())) {
					results[key] = this.champions[key]
				}
			}
			return results
		}
	},
	template:
		`<div class="card" v-if="player.championId != -1">
		<img :src="imageUrl" class="card-img-top">
		<div class="card-body">
			<div class="card-title">{{ champion.name }}</div>
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
						<champion-search-card @champion-selected="player.championId = c.key" v-for="c in championSearchResults" :champion="c"></champion-search-card>
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
		summonerName: "honolulu777",
		championsAreLoaded: false,
		isInGame: false,
		allChampions: {},
		activeGameData: {},
		composition: {
			blue: {
				top: {
					championId: 1
				},
				jgl: {
					championId: -1
				},
				mid: {
					championId: -1
				},
				bot: {
					championId: -1
				},
				sup: {
					championId: -1
				}
			},
			red: {
				top: {
					championId: -1
				},
				jgl: {
					championId: -1
				},
				mid: {
					championId: -1
				},
				bot: {
					championId: -1
				},
				sup: {
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
					console.log("loaded all champions")
					for ([key, value] of Object.entries(response.data.data)) {
						v.allChampions[value.key] = value
					}
					v.championsAreLoaded = true
				})
				.catch(function (error) {
					console.error("error loading all champions " + error)
				})
		},
		loadActiveGameData: function() {
			var v = this

			axios.get(config.api.urls.dynamic.activeGame + v.summonerName)
				.then(function (response) {
					console.log("loaded active game data")
					v.activeGameData = response.data
					v.isInGame = true
				})
				.catch(function (error) {
					v.isInGame = false
				})
		}
	},
	computed: {
		fasd: function() {
			return this.summonerName
		}
	}
})