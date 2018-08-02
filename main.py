import discord
from guild_tools.utils import get_top_fame_reapers, get_fame_reaper_of_week, format_names
import os
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from guild_tools.utils import google_auth_setup

client = discord.Client()


creds = google_auth_setup('client_secret.json')
service = build('sheets', 'v4', http=creds.authorize(Http()))


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content == '!fear top 10':
		fame_reapers = get_top_fame_reapers()
		await client.send_message(message.channel, format_names(fame_reapers))

	if message.content == '!fear most famous':
		highest_earner = get_fame_reaper_of_week()
		await client.send_message(message.channel, format_names(highest_earner))

@client.event 
async def on_ready():
	print('Logged in at {}.'.format(datetime.datetime.now()))
	print(client.user.name)
	print(client.user.id)


client.run(os.environ.get('BOT_TOKEM'))