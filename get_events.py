import urllib.request as req, json
import time
import datetime

def get_daily_events():
	events = dict()
			with req.urlopen(('http://numbersapi.com/')+(month)+('/')+(day)+'/date?json') as url:
			print('Exception occurred ')
	return events