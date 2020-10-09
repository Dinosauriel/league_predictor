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


const championcard = {
	props: ['player', 'champions'],
	computed: {
		champion: function() {
			return this.champions[this.player.championId]
		},
		imageUrl: function() {
			return config.api.urls.static.singleChampion + this.champion.image.full
		}
	},
	template:
		`<div v-if="player.championId != -1">
			{{ player.championId }}
			<img :src="imageUrl">
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
		this.loadActiveGameData()
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