from cal import cal
from sheets import sheets
from datetime import datetime


def make_summery(data):
    return "Worked on the project {worked_on}".format(**data)


def make_description(data):
    return "Worked on {worked_on} for {total_time} hours (with a break of {coffe_break} which makes it {pay_time} hours). I got {total_salery} Shekels.".format(**data)


def fix_time(date, time):
    try:
        return datetime.strptime("{date} {time}".format(date=date, time=time), "%d/%m/%Y %H:%M:%S").isoformat()
    except:
        return datetime.strptime("{date} {time}".format(date=date, time=time), "%d/%m/%Y %H:%M").isoformat()


def add_event(data, cal_ctrl):
    event = {
      'summary': make_summery(data),
      'description': make_description(data),
      'start': {
          'dateTime': fix_time(data['date'], data['start_time']),
          'timeZone': 'Asia/Jerusalem',
      },
      'end': {
          'dateTime': fix_time(data['date'], data['end_time']),
          'timeZone': 'Asia/Jerusalem',
      },
      'reminders': {
        'useDefault': True,
      },
    }
    print(event)
    try:
        event = cal_ctrl.events().insert(calendarId='', body=event).execute()
        print('Event created: {url}'.format(url=event.get('htmlLink')))
    except Exception as e:
        print("[ ERROR ] " + str(event))
        print(e)


def main():
    cal_ctrl = cal.get_cal()
    sheets_ctrl = sheets.get_sheets()
    work_data = sheets.get_work(sheets_ctrl)
    for val in work_data:
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
            print(data)
            add_event(data, cal_ctrl)
        else:
            print("[ WARN ] " + str(val))

if __name__ == "__main__":
    main()
