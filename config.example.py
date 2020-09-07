#your api key obtained from the riot api (https://developer.riotgames.com/)
api_key = "RGAPI-AAAAAA-AAAAAAA"
#summoner name for the match search root (to obtain training data)
root_summoner_name = "summoner name"
#server host (https://developer.riotgames.com/docs/lol)
host = "euw1.api.riotgames.com"

#datadragon link for champions.json
champions_json_url = "http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion.json"

#queue id's - what queue id's should be scraped?
#list of queue ids: http://static.developer.riotgames.com/docs/lol/queues.json
queue_ids = [400, 420, 430, 440]

#request limits for the riot api
requests_per_sec = 20
requests_per_2_minutes = 100

#how many games should be scraped when scrape_games is run once?
games_per_scrape = 1800
#should games additionally be stored as json during scraping for potential later use?
should_lake_games = True