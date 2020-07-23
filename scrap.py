import requests
from bs4 import BeautifulSoup
import sys, codecs
import argparse
import time
from datetime import datetime as dt


def is_inrange(date_from,date_to,date):
	

	date = dt.strptime(date[0:11].strip(), '%Y-%m-%d')

	#print(date_from,date_to,date)

	if(date_from == 0 and date_to == 0):
		return True
	
	elif(date_from != 0 and date_to == 0):
		date_from = dt.strptime(date_from.strip(), '%Y-%m-%d')		
		date_to = date.today()

		if(date_from >= date and date_to <= date):
			return True
		else:
			return False
	
	elif(date_from == 0 and date_to != 0):
		date_to = dt.strptime(date_to.strip(), '%Y-%m-%d')
		
		if(date_to <= date):
			return True
		else:
			return False

	elif(date_from != 0 and date_to != 0):
		date_from = dt.strptime(date_from.strip(), '%Y-%m-%d')
		date_to = dt.strptime(date_to.strip(), '%Y-%m-%d')

		if(date_from >= date and date_to <= date):
			return True
		else:
			return False


parser = argparse.ArgumentParser(description='5chスクレイピングスクリプト')

parser.add_argument('arg1', help='検索ワード')
parser.add_argument('arg2', help='アウトプットファイル')
parser.add_argument('--sort', choices=['create', 'write'], default='create', help="create=スレ立て順,write=書き込み順")
parser.add_argument('--order', choices=['desc', 'asc'], default='desc', help="desc=新しい順,asc=古い順")
parser.add_argument('--sr', default=1, help="何レス以上のスレを取得するか")
parser.add_argument('--active', choices=[0,1], default=2, help="0=過去スレのみ,1=現行のみ,2=すべて")
parser.add_argument('--limit', default=0, help="何スレッド目まで取得するか")
parser.add_argument('--date_from', default=0, help="いつから")
parser.add_argument('--date_to', default=0, help="いつまで")

args = parser.parse_args()

keyword = args.arg1
file_dir = args.arg2
sort = args.sort
order = args.order
sr = str(args.sr)
active = str(args.active)
limit = args.limit
date_from = args.date_from
date_to = args.date_to


if(active == "2"):
	parameter = "q="+keyword+"&sort="+sort+"&order="+order+"&sr="+sr
else:
	parameter = "q="+keyword+"&sort="+sort+"&order="+order+"&sr="+sr+"&active="+active

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
print('https://www.logsoku.com/search?'+parameter)

p = 1
title_list = []
thead_count = 0
print("ログ速URL")
while 1:
	url = 'https://www.logsoku.com/search?'+parameter+'&p='+str(p)
	print(url)
	res = requests.get(url,headers=headers)
	if(res.status_code == 200):
		soup = BeautifulSoup(res.text, 'html.parser')

		title_text = soup.find_all("a", class_="thread")
		date_text = soup.find_all(class_="date")

		i = 0
		j = 1
		for t in title_text:
			inrange = is_inrange(date_to,date_from,date_text[j].text)
			if(limit != 0 and thead_count >= int(limit) or thead_count >= 1 and inrange == False):
				break
			elif(inrange == True):
				title_list.append(title_text[i].get("href"))
				i = i + 1
				thead_count = thead_count + 1
			j = j + 1

		if(limit != 0 and thead_count >= int(limit) or thead_count >= 1 and inrange == False):
			break

		p = p + 1

		time.sleep(2)
	else:
		break

thread = []
print("2chURL")
for t in title_list:
	logsoku = "https://www.logsoku.com"+t
	res = requests.get(logsoku)
	soup = BeautifulSoup(res.text, 'html.parser')
	thread_raw = soup.select("#thread-contents > div > div:nth-child(2) > div:nth-child(1) > div.thread-nav > div > a:nth-child(1)")[0].get("href")
	print(thread_raw)
	thread.append(thread_raw)
	time.sleep(2)


file = open(file_dir, 'a')

print("ファイル書き込み")
for th in thread:
	res = requests.get(th,headers=headers)
	res.encoding = res.apparent_encoding
	soup = BeautifulSoup(res.text, 'html5lib')
	raw = soup.find_all("dd")
	for r in raw:
		file.write(r.text)
	time.sleep(2)

file.close()
print("終了")