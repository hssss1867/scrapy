# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GovSpider(CrawlSpider):
    name = 'gov'
    allowed_domains = ['huhhot.gov.cn']
    start_urls = ['http://www.huhhot.gov.cn/zwgk/zfxxgkzl/zfxxgkmlx/1219/1274/1275/index_74.html']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.huhhot.gov.cn/zwgk/zfxxgkzl/zfxxgkmlx/\d+/t\d+_\d+\.html'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'.*?\.html', restrict_xpaths='//div[@class="pages"]/a'), follow=True),
    )

    def parse_item(self, response):
        item = {}
        item['title'] = response.xpath('//div[@class="zwgkxl_content"]/h3/text()').get().strip()

        print(item)

'''
<a target="_self" href="index_74.html" class="page_sytle">1</a>
<a target="_self" href="index_74_1.html" class="page_sytle">2</a>
http://www.huhhot.gov.cn/zwgk/zfxxgkzl/zfxxgkmlx/202001/t20200109_609687.html
http://www.huhhot.gov.cn/zwgk/zfxxgkzl/zfxxgkmlx/202003/t20200304_625308.html
<a href="../../../202003/t20200304_625309.html" onmouseover="viewHide('divTitle625309',event);" onmouseout="hideHide('divTitle625309');" target="_blank">2019年12月呼市财政本级民生支出月报</a>
'''