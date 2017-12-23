import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from dingdian.items import DingdianItem

class Myspider(scrapy.Spider):

    name = 'dingdian'
    allowed_domains = ['x23us.com']
    start_url = 'http://www.x23us.com/class/'
    end_url = '.html'

    def start_requests(self):
        for i in range(1,11):
            url = self.start_url + str(i) +'_1' + self.end_url
            yield Request(url,self.parse)
        yield Request('http://www.x23us.com/quanben/1',self.parse)

    def parse(self, response):
        #print(response.text)
        max_num = BeautifulSoup(response.text,'lxml').find('div',class_ = 'pagelink').find_all('a')[-1].get_text()
        start_url = str(response.url)[:-7]
        for num in range(1,int(max_num)+1):
            url = start_url + '_' + str(num) + self.end_url
            yield Request(url,callback=self.get_name)

    def get_name(self,response):
        #response.encoding = 'gbk'
        trs = BeautifulSoup(response.text,'lxml').find_all('tr',bgcolor = '#FFFFFF')
        for tr in trs:
            novel_name = tr.find_all('a')[1].get_text()
            novel_url = tr.find_all('a')[0]['href']
            yield Request(novel_url,callback=self.get_chapterurl,meta={'name': novel_name,'url': novel_url})

    def get_chapterurl(self,response):
        #response.encoding = 'gbk'
        item = DingdianItem()
        item['name'] = str(response.meta['name']).replace('\xa0','')
        item['novel_url'] = response.meta['url']
        category = BeautifulSoup(response.text,'lxml').find('div',style = 'width:550px;').find('a').get_text().strip()
        author = BeautifulSoup(response.text,'lxml').find('div',style = 'width:550px;').find_all('td')[1].get_text().strip()
        name_id = BeautifulSoup(response.text,'lxml').find('p',class_ = 'btnlinks').find('a',class_ = 'read')['href'][-6:-1].replace('/','')
        item['category'] = str(category)
        item['author'] = str(author)
        item['name_id'] = str(name_id)
        return item