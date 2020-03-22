# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
import re
class Gov1Spider(scrapy.Spider):
    name = 'gov1'
    allowed_domains = ['huhhot.gov.cn']
    start_urls = ['http://www.huhhot.gov.cn/zwgk/zfxxgkzl/zfxxgkmlx/1219/1274/1275/index_74.html']

    def parse(self, response):
        # link = LinkExtractor(allow=r'.*?\.html',restrict_xpaths='//div[@class="pages"]/a')
        # links = link.extract_links(response)
        # print(links)
        item = {}
        item['href'] = re.findall('<a target="_self".*?(index_74_\d+\.html)', response.body.decode())
        print(item)


'''
<a target="_self" href="index_74_1.html" class="page_sytle">2</a>
'''