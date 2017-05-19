# -*- coding: utf-8 -*-


import sys
import scrapy
import csv
import codecs
import time
import datetime
import shutil
import os
import logging
from scrapy.selector import Selector
from scrapy.http import Request
from amac_spider.items import PrivateFundmeta
from selenium import webdriver
from selenium.webdriver.support.select import Select
from scrapy.utils.log import configure_logging


reload(sys)
sys.setdefaultencoding("utf8")

class PrivateFundSpider(scrapy.Spider):
    name = "privatefund"
    allow_domains = ["ba.amac.org.cn"]
    fund_id_set =  set([])
    driver = None
    custom_settings = {
        "ITEM_PIPELINES": {
            "amac_spider.pipelines.PrivateFundSpiderPipeline": 100
        }
    }
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.WARN
    )
    def start_requests(self):
        # 生成导出csv文件及header。每次都覆盖
        today = datetime.datetime.now()
        today_str =  "%s_%s_%s" % (today.year, today.month,today.day )
        csvName = "fund_list"
        csvFileName = csvName+".csv"
        is_exist =  os.path.exists(csvFileName)
        if is_exist:
            shutil.copyfile(csvFileName, csvName+"_" + today_str + ".csv")
            with open(csvFileName, 'rb') as csv_file:
                reader = csv.reader(csv_file)
                for line in reader:
                    fund_id = line[14]
                    self.fund_id_set.add(fund_id)
                csv_file.close()
        else:
            with open(csvFileName, 'wb') as csv_file:
                csv_file.write(codecs.BOM_UTF8)
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(
                    [u'基金名称', u'基金编号', u'成立时间', u'备案时间', u'基金备案阶段', u'基金类型',
                     u'币种', u'基金管理人名称', u'管理类型', u'托管人名称', u'主要投资领域', u'运作状态',
                     u'基金信息最后更新时间', u'基金协会特别提示',u'ID'])
        url = "http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html"
        self.driver = webdriver.PhantomJS()
        # self.driver = webdriver.Chrome()
        # self.driver = webdriver.Firefox()
        yield Request(url, callback=self.parse_index)

    def parse_index(self, response):
        self.driver.get(response.url)
        time.sleep(8)
        btn = self.driver.find_elements_by_class_name("ui-button-text-only")
        btn[0].click()

        sel = self.driver.find_element_by_xpath("//select[@name='fundlist_length']")
        Select(sel).select_by_value("100")

        startPage = 1
        self.driver.execute_script("document.getElementById('goInput').value=%d;" %startPage)
        btnGo = self.driver.find_elements_by_class_name("btn-go")
        btnGo[0].click()

        time.sleep(2)
        pager = self.driver.find_element_by_id("fundlist_info").text
        pager = pager.split("，")[1]
        pager = pager[1:len(pager)-1]
        pages = int(pager)
        # 首页获取
        id_set = self.fund_id_set
        name_links = self.driver.find_elements_by_xpath("//a[@class='ajaxify']")
        for link in name_links:
            try:
                href = link.get_attribute("href")
                if "manager" not in href:
                    fund_id = self.get_fund_id(href)
                    if not id_set.__contains__(fund_id):
                        #time.sleep(0.1)
                        yield Request(href, callback=self.parse_fundinfo, dont_filter=True)
            except Exception, e:
                print Exception, ":", e
        # 逐页获取
        for i in range(startPage, pages):
            el = self.driver.find_elements_by_class_name("next")
            if el:
                el[0].click()
                time.sleep(0.5)
                name_links = self.driver.find_elements_by_xpath("//a[@class='ajaxify']")
                for link in name_links:
                    try:
                        href = link.get_attribute("href")
                        if "manager" not in href:
                            fund_id = self.get_fund_id(href)
                            if not id_set.__contains__(fund_id):
                                #time.sleep(0.1)
                                yield Request(href, callback=self.parse_fundinfo, dont_filter=True)
                    except Exception, e:
                        print Exception, ":", e
            else:
                print("can not find next btn")
        self.driver.close()

    def get_fund_id(self,url):
        lastIndex = len(url) - 5
        fundId = url[49:lastIndex]
        return fundId

    def parse_fundinfo(self, response):
        fund_items = []
        try:
            sel = Selector(response)
            parents = sel.xpath('//td[@class="td-content"]|//td[@class="td-content"]/a')
            i = 0
            contents = []
            for p in parents:
                ff = p.xpath('text()').extract()
                if len(ff) > 0:
                    contents.append(ff[0])
                else:
                    contents.append("")
            len(contents)
            fund = PrivateFundmeta()
            fund["fundId"] = self.get_fund_id(response.url)
            fund['fundName'] = contents[0]
            fund['fundCode'] = contents[1]
            fund['setupDate'] = contents[2]
            fund['recordDate'] = contents[3]
            fund['recordStep'] = contents[4]
            fund['fundType'] = contents[5]
            fund['currency'] = contents[6]
            fund['managerName'] = contents[8]
            fund['manageType'] = contents[9]
            fund['trusteeName'] = contents[10]
            fund['investArea'] = contents[11]
            fund['status'] = contents[12]
            fund['lastModifiedTime'] = contents[13]
            fund['specialSuggest'] = contents[14]
            fund_items.append(fund)
        except Exception, e:
            print Exception, ":", e
        return fund_items

    def close(spider, reason):
        print 'onclose'