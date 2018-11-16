import urllib.request as req, json
import time
import datetime

def get_daily_events():
	events = dict()
	today = datetime.date.today()
	day = today.strftime('%d')
	month = today.strftime('%m')
	for i in range(500):
		try:
			with req.urlopen(('http://numbersapi.com/')+(month)+('/')+(day)+'/date?json') as url:
				data = json.loads(url.read().decode())
				events[int(data['year'])] = data['text']
				time.sleep(1)
		except Exception:
			print('Exception occurred ')
	return events