import requests
import environ
from discord_bot.settings import API_KEY

headers = {'Authorization': API_KEY, 'Accept':'application/vnd.api+json'}

def retrieve_player_info(player_name):
	if ''.join(list(filter(lambda x: x.isalpha() or x == '_', list(player_name)))) != player_name:
		return 
	else:
		return requests.get('https://api.dc01.gamelockerapp.com/shards/na/players/', 
		headers=headers, params={'filter[playerNames]':'{}'.format(player_name)})

def retrieve_match_telemetry(match_id):
	pass

def retrieve_match_data(match_id):
	pass
