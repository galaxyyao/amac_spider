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
