# -*- coding: utf-8 -*-

import urllib2
import os
import re
import codecs
import json
import sys
import scrapy
import csv
import codecs
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from private_product_spider.items import Productmeta

reload(sys)
sys.setdefaultencoding("utf8")


class PrivateProductSpider(scrapy.Spider):
    name = "privateproduct"
    allow_domains = ["ba.amac.org.cn"]
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-US,en;q=0.8,zh-CN;q=0.6",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "ba.amac.org.cn",
            "origin": "http://ba.amac.org.cn",
            "referer": "http://ba.amac.org.cn/pages/amacWeb/web-list.html",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        },
        "ITEM_PIPELINES": {
            "private_product_spider.pipelines.PrivateProductSpiderPipeline": 100
        }
    }
    is_first_request = True

    def start_requests(self):
        # 生成导出csv文件及header。每次都覆盖
        with open('private_product_list.csv', 'wb') as csv_file:
            csv_file.write(codecs.BOM_UTF8)
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(
                [u'序号', u'产品数字编号', u'产品编码', u'产品名称', u'管理机构', u'设立日期', u'到期日', u'投资类型', u'是否分级', u'管理方式', u'成立规模',
                 u'成立时参与户数', u'托管机构', u'份额登记机构', u'投资范围'])

        url = "http://ba.amac.org.cn/pages/amacWeb/user!list.action"
        formdata = {
            "filter_LIKES_CPMC": "",
            "filter_LIKES_GLJG": "",
            "filter_LIKES_CPBM": "",
            "filter_GES_SLRQ": "",
            "filter_LES_SLRQ": "",
            "page.searchFileName": "publicity_web",
            "page.sqlKey": "PAGE_PUBLICITY_WEB",
            "page.sqlCKey": "SIZE_PUBLICITY_WEB",
            "nd": "1490147595367",
            "page.pageSize": "50",
            "page.pageNo": "1",
            "page.orderBy": "SLRQ",
            "page.order": "desc"
        }
        yield FormRequest(url, callback=self.parse_productmeta, formdata=formdata, dont_filter=True)

    def parse_productmeta(self, response):
        json_body = json.loads(response.body)
        if (self.is_first_request):
            self.is_first_request = False
            total_page = int(json_body['totalPages'])
            return self.do_formal_request(total_page)
        productmetas = json_body['result']
        productmeta_items = []
        for dict in productmetas:
            productmeta_item = Productmeta()
            productmeta_item['RN'] = dict['RN']
            productmeta_item['PW_ID'] = dict['PW_ID']
            productmeta_item['MPI_ID'] = dict['MPI_ID']
            productmeta_item['PW_STATES'] = dict['PW_STATES']
            productmeta_item['CPMC'] = dict['CPMC']
            productmeta_item['CPBM'] = dict['CPBM']
            productmeta_item['GLJG'] = dict['GLJG']
            productmeta_item['SLRQ'] = dict['SLRQ']
            productmeta_item['DQR'] = dict['DQR'],
            productmeta_item['TZLX'] = dict['TZLX']
            productmeta_item['SFFJ'] = dict['SFFJ']
            productmeta_item['GLFS'] = dict['GLFS']
            productmeta_item['CLGM'] = dict['CLGM']
            productmeta_item['CLSCYHS'] = dict['CLSCYHS']
            productmeta_item['TGJG'] = dict['TGJG']
            productmeta_item['FEDJJG'] = dict['FEDJJG']
            productmeta_item['TZFW'] = dict['TZFW']
            productmeta_items.append(productmeta_item)
        return productmeta_items

    def do_formal_request(self, total_page):
        url = "http://ba.amac.org.cn/pages/amacWeb/user!list.action"
        for i in range(1, total_page + 1):
            formdata = {
                "filter_LIKES_CPMC": "",
                "filter_LIKES_GLJG": "",
                "filter_LIKES_CPBM": "",
                "filter_GES_SLRQ": "",
                "filter_LES_SLRQ": "",
                "page.searchFileName": "publicity_web",
                "page.sqlKey": "PAGE_PUBLICITY_WEB",
                "page.sqlCKey": "SIZE_PUBLICITY_WEB",
                "nd": "1490147595367",
                "page.pageSize": "50",
                "page.pageNo": str(i),
                "page.orderBy": "SLRQ",
                "page.order": "desc"
            }
            yield FormRequest(url, callback=self.parse_productmeta, formdata=formdata, dont_filter=True)

    def close(spider, reason):
        print 'onclose'