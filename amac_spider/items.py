# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class Productmeta(scrapy.Item):
    RN = scrapy.Field()
    PW_ID = scrapy.Field()
    MPI_ID = scrapy.Field()
    PW_STATES = scrapy.Field()
    CPMC = scrapy.Field()
    CPBM = scrapy.Field()
    GLJG = scrapy.Field()
    SLRQ = scrapy.Field()
    DQR = scrapy.Field()
    TZLX = scrapy.Field()
    SFFJ = scrapy.Field()
    GLFS = scrapy.Field()
    CLGM = scrapy.Field()
    CLSCYHS = scrapy.Field()
    TGJG = scrapy.Field()
    FEDJJG = scrapy.Field()
    TZFW = scrapy.Field()

class PrivateFundmeta(scrapy.Item):
    fundId = scrapy.Field()
    fundName = scrapy.Field()
    fundCode = scrapy.Field()
    setupDate = scrapy.Field()
    recordDate = scrapy.Field()
    recordStep = scrapy.Field()
    fundType = scrapy.Field()
    currency = scrapy.Field()
    managerName = scrapy.Field()
    manageType = scrapy.Field()
    trusteeName = scrapy.Field()
    investArea = scrapy.Field()
    status = scrapy.Field()
    lastModifiedTime = scrapy.Field()
    specialSuggest = scrapy.Field()