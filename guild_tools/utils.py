import os
import operator
from oauth2client import file, client, tools
import logging
import json

spreadsheet_id = os.environ.get('SPREADSHEET_ID')

def google_auth_setup():
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	with open('cred_file.json' , 'w') as file:
		json.dump(os.environ.get('GOOGLE_CREDS'), file)
	try:
	    flow = client.flow_from_clientsecrets(os.path.join(os.getcwd(), 'cred_file.json'), SCOPES)
	    flags = tools.argparser.parse_args('--auth_host_name localhost --logging_level INFO'.split())
	    creds = tools.run_flow(flow, store, flags)
	except:
		logging.exception('')
		return None
	else:
		return creds

#calculate at 00:00 AM and store in env vars
def get_fame_reaper_of_week():
	request = service.spreadsheets().get(spreadsheetId=spreadsheet_id)
	response = request.execute()	
	
	sheet_list = [sheet['properties']['title'] for sheet in response['sheets']]
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

	sheet_list = [sheet['properties']['title'] for sheet in response['sheets']]
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

	weekly_fame_list_with_name.sort(key=operator.itemgetter(1))
	weekly_fame_list_without_duplicates = list(dict(weekly_fame_list_with_name).items())
	weekly_fame_list_without_duplicates.sort(key=operator.itemgetter(1))
	top_ten = weekly_fame_list_without_duplicates[-11:][::-1]

	return top_ten

def get_player_names():
	request = service.spreasheets().get(spreadsheet_id=spreadsheet_id)
	response = request.execute()

	last_sheet = response['sheets'][-1]['properties']['title']
	names = '{}!A2:A51'.format(last_sheet)

	request = service.spreadsheets().get(spreadsheet_id=spreadsheet_id, ranges=names, includeGridData=True)
	response = request.execute()

	return 

def format_names(names):
	if isinstance(names, tuple):
		return '{} - {}'.format(names[0], names[1])

	elif isinstance(names, list):
		names_string = ''
		for name in names:
			names_string += '{} - {} \n'.format(name[0], name[1]) 

	return names_string