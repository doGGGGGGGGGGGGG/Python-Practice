import requests
from bs4 import BeautifulSoup
import traceback
import re
#http://quote.eastmoney.com/stocklist.html 列表来源
#https://gupiao.baidu.com/stock/ 信息来源


def GetHtmlText(url, code = "utf-8"):
	try:
		r = r.requests.get(url, timeout = 30)
		r.raise_for_stauts()
		r.encoding = code
		return r.text
	except:
	    return ""


def GetStockList(lst, stockURL):  #获取列表信息
	html = GetHtmlText(stockURL, "GB2312")
	soup = BeautifulSoup(html, "html.parser")
	a = soup.find_all("a")
	for i in a:
		try:
			href = i.attrs["href"]
			lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
		except:
			continue


def GetStockInfo(lst, stockURL, fpath):  #获取个股信息并存储
	count = 0
	for stock in lst:
		url = stockURL + stock + "html"
		html = GetHtmlText(url)
		try:
			if html == "":
				continue
			infoDict = {}
			soup = BeautifulSoup(html, "html.parser")
			stockInfo = soup.find("div", attrs = {"class":"stock-bets"})
			name = stockInfo.find_all(attrs = {"class":"bets-name"})[0]
			infoDict.update({"股票名称":name.text.split()[0]})
			keyList = stockInfo.find_all("dt")
			valueList = stockInfo.find_all("dd")
			for i in range(len(keyList)):
				key = keyList[i].text
				val = valueList[i].text
				infoDict[key] = val
			with open(fpath, "a", encoding = "utf-8") as f:
				f.write(str(infoDict) + "\n")
				count += 1
				print("\r当前进度：{:.af}%".format(count*100/len(lst)), end = "")
		except:
			count += 1
			print("\r当前进度：{:.af}%".format(count*100/len(lst)), end = "")
			continue


def main():
	stock_list_url = "http://quote.eastmoney.com/stocklist.html"
	stock_info_url = "https://gupiao.baidu.com/stock/"
	output_file = "C://StockInfo.txt"
	slist = []
	GetStockList(slist, stock_list_url)
	GetStockInfo(slist, stock_info_url, output_file)


main()