
var config = {
	api: {
		urls: {
			static: {
				allChampions: "https://ddragon.leagueoflegends.com/cdn/10.20.1/data/en_US/champion.json"
			},
			dynamic: {
				activeGame: "/active-game/"
			}
		}
	}
}


var app = new Vue({
	el: "#app",
	data: {
		championsAreLoaded: false,
		isInGame: false,
		allChampions: {},
		activeGameData: {}
	},
	created: function() {
		this.loadAllChampions()
		this.loadActiveGameData()
	},
	methods: {
		loadAllChampions: function() {
			var v = this

			axios.get(config.urls.static.allChampions)
				.then(function (response) {
					console.log("loaded all champions")
					v.allChampions = response.data.data
					v.championsAreLoaded = true
				})
				.catch(function (error) {
					console.error("error loading all champions " + error)
				})
		},
		loadActiveGameData: function() {
			var v = this

			axios.get(config.urls.local.allGameData)
				.then(function (response) {
					console.log("loaded active game data")
					v.activeGameData = response.data
					v.isInGame = true
				})
				.catch(function (error) {
					console.error("error loading active game data " + error)
					v.isInGame = false
				})
		}
	},
	computed: {
		summonerName: function() {
			return this.activeGameData.activePlayer.summonerName
		}
	}
})