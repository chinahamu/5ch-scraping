import requests
from bs4 import BeautifulSoup
import sys, codecs

args = sys.argv
keyword = args[1]
file_dir = args[2]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
print('https://www.logsoku.com/search?q='+keyword+'&sr=10')

res = requests.get('https://www.logsoku.com/search?q='+keyword+'&sr=10',headers=headers)

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