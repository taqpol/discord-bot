import requests
from discord_bot.settings import API_KEY

def get_player_elo(player_info):
	return player_info.json()['data'][0]['attributes']['stats']['rankPoints']

