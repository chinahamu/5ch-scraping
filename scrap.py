import requests
from bs4 import BeautifulSoup
import sys, codecs
import argparse

parser = argparse.ArgumentParser(description='5chスクレイピングスクリプト')

parser.add_argument('arg1', help='検索ワード')
parser.add_argument('arg2', help='アウトプットファイル')
parser.add_argument('--sort', choices=['create', 'write'], default='create', help="create=スレ立て順,write=書き込み順")
parser.add_argument('--order', choices=['desc', 'asc'], default='desc', help="desc=新しい順,asc=古い順")
parser.add_argument('--sr', default=1, help="何スレ以上のスレを取得するか")
parser.add_argument('--active', choices=[0,1], default=2, help="0=過去スレのみ,1=現行のみ,2=すべて")

args = parser.parse_args()

keyword = args.arg1
file_dir = args.arg2
sort = args.sort
order = args.order
sr = str(args.sr)
active = str(args.active)

if(active == "2"):
	parameter = "q="+keyword+"&sort="+sort+"&order="+order+"&sr="+sr
else:
	parameter = "q="+keyword+"&sort="+sort+"&order="+order+"&sr="+sr+"&active="+active


print(parameter)



headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
print('https://www.logsoku.com/search?'+parameter)

res = requests.get('https://www.logsoku.com/search?'+parameter,headers=headers)

soup = BeautifulSoup(res.text, 'html.parser')

title_text = soup.find_all("a", class_="thread")

title_list = []

i = 0
for t in title_text:
	title_list.append(title_text[i].get("href"))
	i = i + 1

thread = []
for t in title_list:
	logsoku = "https://www.logsoku.com"+t
	res = requests.get(logsoku)
	soup = BeautifulSoup(res.text, 'html.parser')
	thread_raw = soup.select("#thread-contents > div > div:nth-child(2) > div:nth-child(1) > div.thread-nav > div > a:nth-child(1)")[0].get("href")
	thread.append(thread_raw)


file = open(file_dir, 'a')

for th in thread:
	res = requests.get(th,headers=headers)
	res.encoding = res.apparent_encoding
	soup = BeautifulSoup(res.text, 'html5lib')
	raw = soup.find_all("dd")
	for r in raw:
		file.write(r.text)

file.close()