from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
from discord_bot.settings import SPREADSHEET_ID as spreadsheet_id
import operator
# Setup the Sheets API


def google_auth_setup(cred_file):
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	try:
	    flow = client.flow_from_clientsecrets(cred_file, SCOPES)
	    flags = tools.argparser.parse_args('--auth_host_name localhost --logging_level INFO'.split())
	    creds = tools.run_flow(flow, store, flags)
	except:
		return None
	else:
		return creds

creds = google_auth_setup('client_secret.json')
service = build('sheets', 'v4', http=creds.authorize(Http()))


#calculate at 00:00 AM and store in env vars
def get_fame_reaper_of_week():
	request = service.spreadsheets().get(spreadsheetId=spreadsheet_id)
	response = request.execute()	
	
	sheet_list = [sheet['sheets'][position]['properties']['title'] for sheet in response['sheets']]
	ranges = '{}!A2:B51'.format(sheet_list[-1])  
	major_dimension = 'COLUMNS'

	request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=ranges, majorDimension=major_dimension)
	response = request.execute()

	response['values'][1] = list(map(lambda x: int(x), response['values'][1]))
	top_fame = max(response['values'][1])
	position = response['values'][1].index(top_fame)

	return (response['values'][0][position], top_fame)

#recalculate at 00:00 AM Monday asynchronously; do not attempt before and only attempt once
def get_top_fame_reapers():
	request = service.spreadsheets().get(spreadsheetId=spreadsheet_id)
	response = request.execute()

	#series of steps required to get weekly fame for user at position for x sheet
	# response['sheets'][x]['data'][0]['rowData'][position]['values'][1]['effectiveValue']['numberValue']

	sheet_list = [sheet['properties']['title'] for sheet in response['sheets']]
	#candidate for possible conversion to f strings when possible
	fame_range = ['{}!A2:D51'.format(sheet) for sheet in sheet_list]

	request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=fame_range, includeGridData=True)
	response = request.execute()

	weekly_fame_list_with_name = []
	for sheets in range(len(response['sheets'])):
		for players in range(50):
			try:
				name_and_fame = (response['sheets'][sheets]['data'][0]['rowData'][players]['values'][0]['effectiveValue']['stringValue'],
					response['sheets'][sheets]['data'][0]['rowData'][players]['values'][1]['effectiveValue']['numberValue'])
			except:
				break
			else:
				try:
					last_week_fame = response['sheets'][sheets]['data'][0]['rowData'][players]['values'][3]['effectiveValue']['numberValue']
				except:
					pass
				else:
					if not last_week_fame:
						pass
					else:
						weekly_fame_list_with_name.append(name_and_fame)

	weekly_fame_list_with_name.sort(key=operator.itemgetter(1), reverse=True)
	import pdb; pdb.set_trace()

	return weekly_fame_list_with_name[:10]



