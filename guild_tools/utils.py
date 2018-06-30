from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
from settings import spreadsheet_id
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



def get_fame_reaper_of_week(range=None):
	ranges = '6/24/18!A2:C51'  
	major_dimension = 'COLUMNS'

	request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=ranges, majorDimension=major_dimension)
	response = request.execute()

	response['values'][1] = list(map(lambda x: int(x), response['values'][1]))
	position = response['values'][1].index(max(response['values'][1]))

	return response['values'][0][position]

def get_top_fame_reapers():
	request = service.spreadsheets().get(spreadsheetId=spreadsheet_id)
	response = request.execute()

	#series of steps required to get weekly fame for user at position for one week
	# response['sheets'][0]['data'][0]['rowData'][position]['values'][1]['effectiveValue']['numberValue']

	sheet_list = [response['sheets'][position]['properties']['title'] for position in range(len(response['sheets']))]
	fame_range = ['{}!A2:C51'.format(sheet) for sheet in sheet_list]

	request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=fame_range, includeGridData=True)
	response = request.execute()

