import urllib.request
import urllib.error
import re
import pymysql
class Spider(object):
	def __init__(self):
		self.conn = pymysql.connect(host='192.168.195.128',user='Ubuntu',passwd='87110346',db='mysql',charset='utf8')
		self.cur = self.conn.cursor()
		self.cur.execute("use spider")
	def loadPage(self,page):
		#目标网站：https://www.qiushibaike.com/text/page/13/
		url = "https://www.qiushibaike.com/text/page/"+str(page)
		#进行反爬虫策略
		#1伪装代理
		proxy = urllib.request.ProxyHandler({'http':'115.46.64.249:8123'})
		opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
		#伪装头部
		headers = ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36')
		opener.addheaders = [headers]
		urllib.request.install_opener(opener)

		#异常处理
		try:
			response = urllib.request.urlopen(url)
			html = response.read()
		
		except urllib.error.URLError as e:
			if hasattr(e,"code"):
				print(e.code)
			if hasattr(e,"reason"):
				print(e.reason)
		data= html.decode('utf-8',"ignore")
		# pattern = re.compile(r'<div class="content">(.*?)</div',re.S)
		# item_list = pattern.findall(gbk_html)
		# print(item_list)
		return data
	def printOnePage(self,item_list,page):
		print("****第%d页爬去完毕*****"%page)
		for item in item_list:
			print("====================")
			item = item.replace("<span>","").replace("</span>","").replace("<br>","").replace("<br/>","")
			print(item)
	def nameData(self,data):
		#<a href="/users/23762049/" target="_blank" onclick="_hmt.push(['_trackEvent','web-list-author-text','chick'])">
# <h2>
# 我是你夏姐姐呀
# </h2>
# </a>
#<img src="//pic.qiushibaike.com/system/avtnew/2376/23762049/thumb/20180725210619.jpg?imageView2/1/w/90/h/90" alt="我是你夏姐姐呀">
		pattern = re.compile(r'<img src="//pic.qiushibaike.com/system.*?" alt="(.*?)">')
		name_list = pattern.findall(data)

		return name_list
	def contentData(self,data):
		pattern = re.compile(r'<div class="content">(.*?)</div',re.S)
		new_list = []
		item_list = pattern.findall(data)
		for item in item_list:
			item = item.replace("<span>","").replace("</span>","").replace("<br>","").replace("<br/>","")
			new_list.append(item)

		return new_list
	def writedatabase(self,datalist):
		
			
		try:
			for item in datalist:
				print(item[0],item[1])
				self.cur.execute("insert into qiushi values(0,\"%s\",\"%s\")"%(item[0],item[1]))
				self.cur.connection.commit()
		
		finally:
			self.cur.close()
			self.conn.close()


if __name__ == '__main__':
	mySpider = Spider()
	data=mySpider.loadPage(1)
	namelist = mySpider.nameData(data)
	contentlist = mySpider.contentData(data)
	datalist = [(name,content) for name in namelist for content in contentlist if namelist.index(name)==contentlist.index(content)]
	#print(datalist)
	mySpider.writedatabase(datalist)