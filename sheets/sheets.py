from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from os.path import isfile
import json
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'


def get_sheets():
    store = file.Storage('/home/itay/Documents/projects/programing/Python/log_work_to_calandar/sheets/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/home/itay/Documents/projects/programing/Python/log_work_to_calandar/sheets/sheets_credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('sheets', 'v4', http=creds.authorize(Http()))


def get_work(sheets_service):
    out = list()
    if isfile("/home/itay/Documents/projects/programing/Python/log_work_to_calandar/used.json"):
        with open('/home/itay/Documents/projects/programing/Python/log_work_to_calandar/used.json') as f:
            used = json.load(f)
    else:
        used = []
    SPREADSHEET_ID = ''
    all_sheets = sheets_service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID, ranges=[]).execute()['sheets']
    for sheet in all_sheets:
        if sheet['properties']['title'] != "מעקב עצמי":
            RANGE_NAME = sheet['properties']['title'] + '!A2:K'  # last table in the data section
            result = sheets_service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()  # work data
            for e in result.get('values', []):
                if e not in used:
                    out.append(e)
                    used.append(e)
    with open('/home/itay/Documents/projects/programing/Python/log_work_to_calandar/used.json', "w") as f:
        used = json.dump(used, f)
    return out


def main(sheets_service):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    values = get_work(sheets_service)
    if not values:
        print('No data found.')
    else:
        print("date, start_time, end_time, coffe_break, total_time, pay_time, holiday, drivings, salery_per_hour, total_salery, worked_on")
        for val in values:
                if len(val) >= 10:
                    data = {"date": val[0],
                        "start_time": val[1],
                        "end_time": val[2],
                        "coffe_break": val[3],
                        "total_time": val[4],
                        "pay_time": val[5],
                        "holiday": val[6],
                        "drivings": val[7],
                        "salery_per_hour": val[8],
                        "total_salery": val[9],
                        "worked_on": ""}
                if len(val) == 11:
                    data["worked_on"] = val[10]
                if len(val) >= 10:
                    print("{date}, {start_time}, {end_time}, {coffe_break}, {total_time}, {pay_time}, {holiday}, {drivings}, {salery_per_hour}, {total_salery}, {worked_on}".format(**data))


if __name__ == '__main__':
    main(get_sheets())
