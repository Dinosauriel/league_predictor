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
		summonerName: "honolulu777",
		championsAreLoaded: false,
		isInGame: false,
		allChampions: {},
		activeGameData: {},
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

	}
})