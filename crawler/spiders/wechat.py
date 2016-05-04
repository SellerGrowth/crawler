# -*- coding: utf-8 -*-
import json
import scrapy
import HTMLParser
from crawler.items import *

class WechatSpider(scrapy.Spider):
    name = "wechat"
    allowed_domains = [
        "weixin.sogou.com",
        "mp.weixin.qq.com"
    ]
    start_urls = [
        #'http://weixin.sogou.com/weixin?type=1&query=TRADERONLINE',
        'http://weixin.sogou.com/weixin?type=1&query=i_kuajing',
        #'http://weixin.sogou.com/weixin?type=1&query=cifnews',
        #'http://weixin.sogou.com/weixin?type=1&query=Pony-2014',
        #'http://weixin.sogou.com/weixin?type=1&query=kjds360',
        #'http://weixin.sogou.com/weixin?type=1&query=hiwto123',
        #'http://weixin.sogou.com/weixin?type=1&query=dianshangwin_com',
        #'http://weixin.sogou.com/weixin?type=1&query=KJDS_com',
        #'http://weixin.sogou.com/weixin?type=1&query=haixianhui888',
        #'http://weixin.sogou.com/weixin?type=1&query=STLB-36HAPPY',
        #'http://weixin.sogou.com/weixin?type=1&query=BL-51WAY',
        #'http://weixin.sogou.com/weixin?type=1&query=baimawar',
        #'http://weixin.sogou.com/weixin?type=1&query=szcbea',
        #'http://weixin.sogou.com/weixin?type=1&query=focusorder',
        #'http://weixin.sogou.com/weixin?type=1&query=qhkjds',
        #'http://weixin.sogou.com/weixin?type=1&query=valuelinkgroup',
        #'http://weixin.sogou.com/weixin?type=1&query=jinkoulaowai',
        #'http://weixin.sogou.com/weixin?type=1&query=sz321sxy',
        #'http://weixin.sogou.com/weixin?type=1&query=Pony-2006',
        #'http://weixin.sogou.com/weixin?type=1&query=haiyinhui',
    ]

    def parse(self, response):
        results = response.css('div.wx-rb')
        for r in results:
            sr = SogouResultItem()
            sr['title'] = r.xpath('//h3/descendant::text()').extract()[0]
            sr['link'] = r.xpath('@href').extract()[0]
            sr['desc'] = ''.join(r.xpath("div[@class='txt-box']/p[@class='s-p3']/span[@class='sp-txt']/descendant::text()").extract())
            #print dict(sr)
            req = scrapy.Request(sr['link'], callback=self.parse_wechat)
            req.meta['item'] = sr
            yield req

    def parse_wechat(self, response):
        html_parser = HTMLParser.HTMLParser()
        nickname = response.css('strong.profile_nickname::text').extract()[0].strip()
        msgs = response.xpath('//script').re('var\smsgList = \'(.*)\'')[0]
        msgs_json = json.loads(msgs)
        msg_list = msgs_json.get('list', [])
        for msg in msg_list:
            app_msg_info = msg.get('app_msg_ext_info', {})
            comm_msg_info = msg.get('comm_msg_info', {})

            dt = comm_msg_info.get('datetime', None)
            if not dt:
                continue

            if app_msg_info.get('fileid', 0) != 0:
                writem = WechatResultItem()
                writem['title'] = app_msg_info.get('title', '')
                writem['link'] = 'http://mp.weixin.qq.com/' + app_msg_info.get('content_url', '')
                writem['datetime'] = dt
                writem['digest'] = app_msg_info.get('digest', None)
                writem['cover'] = app_msg_info.get('cover', None)
                writem['author'] = app_msg_info.get('author', None)
                writem['source'] = nickname
                writem['fileid'] = app_msg_info.get('fileid',0)
                yield writem

            for m in app_msg_info.get('multi_app_msg_item_list', []):
                writem = WechatResultItem()
                writem['title'] = m.get('title', '')
                writem['link'] = 'http://mp.weixin.qq.com/' + html_parser.unescape(m.get('content_url', ''))
                writem['datetime'] = dt
                writem['digest'] = m.get('digest', None)
                writem['cover'] = m.get('cover', None)
                writem['author'] = m.get('author', None)
                writem['source'] = nickname
                writem['fileid'] = m.get('fileid',0)
                yield writem

        #filename = response.url.split("/")[-2] + '.html'
        #with open(filename, 'w') as f:
        #    json.dump(msg_list, f, indent=4)
