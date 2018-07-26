import requests
import os

API_KEY = os.environ.get('API_KEY')

headers = {'Authorization': API_KEY, 'Accept':'application/vnd.api+json'}

def get_player_elo(player_info):
	return player_info.json()['data'][0]['attributes']['stats']['rankPoints']


def retrieve_player_info(player_name):
	if ''.join(list(filter(lambda x: x.isalpha() or x == '_', list(player_name)))) != player_name:
		response = requests.Response()
		response.status_code = 400
		response.reason = 'Bad Request'
		return response
	else:
		return requests.get('https://api.dc01.gamelockerapp.com/shards/na/players/', 
		headers=headers, params={'filter[playerNames]':'{}'.format(player_name)})


def retrieve_match_telemetry(match_id):
	pass


def retrieve_match_data(match_id):
	pass

