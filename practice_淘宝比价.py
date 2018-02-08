import requests
import re
#https://s.taobao.com/search?q=手机


def GetHtmlText(url):
	try:
		r = requests.get(url, timeout = 30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""


def ParsePage(ilt, html):
	try:
		plt = re.findall(r'"price":"[\d.]*"', html)
		tlt = re.findall(r'"title":".*?"', html)
		for i in range(len(plt)):
			price = eval(plt[i].split(":")[1])  #去掉双引号
			title = eval(tlt[i].split(":")[1])
			ilt.append([price, title])
	except:
		return ""


def PrintGoodsList(ilt):
	tplt = "{:4}\t{:8}\t{:16}"
	print(tplt.format("序号", "价格", "商品名称"))
	count = 0
	for g in ilt:
		count += 1
		print(tplt.format(count, g[0], g[1]))


def main():
	goods = "手机"
	depth = 2
	start_url = "https://s.taobao.com/search?q=" + goods
	infoList = []
	for i in range(depth):
		try:
			url = start_url + "&s=" + str(48*i)
			html = GetHtmlText(url)
			ParsePage(infoList, html)
		except:
			continue
	PrintGoodsList(infoList)

main()