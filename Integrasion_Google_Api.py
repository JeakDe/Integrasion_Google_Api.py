from __future__ import print_function
import datetime
import time

import schedule
import telebot
import httplib2
from googleapiclient.discovery import build
import config
from oauth2client.service_account import ServiceAccountCredentials
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
def job():
    bot = telebot.TeleBot(config.TOKEN)

    def main():
        print("I'm working...")
        creds = ServiceAccountCredentials.from_json_keyfile_name(config.client_secret_calendar, 'https://www.googleapis.com/auth/calendar.readonly')
        http = creds.authorize(httplib2.Http())
        service = build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        now_1day = round(time.time()) + 86400  # плюс сутки
        now_1day = datetime.datetime.fromtimestamp(now_1day).isoformat() + 'Z'
        eventsResult = service.events().list(
            calendarId='lebronjames24542565@gmail.com', timeMin=now, timeMax=now_1day, maxResults=100,
            singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        if not events:
            print('нет событий на ближайшие сутки')
            bot.send_message("1237763001", 'нет событий на ближайшие сутки')
        else:
            msg = '<b>События на ближайшие сутки:</b>\n'
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, ' ', event['summary'])
                if not event['description']:
                    print('нет описания')
                    ev_desc = 'нет описания'
                else:
                    print(event['description'])
                    ev_desc = event['description']

                ev_title = event['summary']
                cal_link = '<a href="%s">Подробнее...</a>' % event['htmlLink']
                ev_start = event['start'].get('dateTime')
                ev_start = ev_start[:-9]
                print(cal_link)
                msg = msg + '%s\n%s\n%s\n%s\n\n' % (ev_title, ev_start, ev_desc, cal_link)
                print('===================================================================')
            bot.send_message("1237763001", msg, parse_mode = 'HTML')

    main()
#    if __name__ == '__main__':
#        main()
print('Listening ...')
schedule.every(1).minutes.do(job)
#schedule.every().hour.do(job)
#schedule.every().day.at("02:36").do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)


