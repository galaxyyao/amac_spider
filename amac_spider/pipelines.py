# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import codecs


class PrivateProductSpiderPipeline(object):
    def process_item(self, item, spider):
        RN = item['RN']
        PW_ID = item['PW_ID']
        MPI_ID = item['MPI_ID']
        PW_STATES = item['PW_STATES']
        CPMC = item['CPMC']
        CPBM = item['CPBM']
        GLJG = item['GLJG']
        SLRQ = item['SLRQ']
        DQR = item['DQR'][0]
        TZLX = item['TZLX']
        SFFJ = item['SFFJ']
        GLFS = item['GLFS']
        CLGM = item['CLGM']
        CLSCYHS = item['CLSCYHS']
        TGJG = item['TGJG']
        FEDJJG = item['FEDJJG']
        TZFW = (item['TZFW']).replace('<br/>','').replace('\r','')
        with open('private_product_list.csv', 'ab+') as csv_file:
            csv_file.write(codecs.BOM_UTF8)
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(
                [RN, MPI_ID, CPBM, CPMC, GLJG, SLRQ, DQR, TZLX, SFFJ, GLFS, CLGM, CLSCYHS, TGJG,
                 FEDJJG, TZFW])
        return item
