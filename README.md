# amac private fund & product spider
scrapy spider for http://www.amac.org.cn/xxgs/

private fund: 私募基金公示
页面：http://ba.amac.org.cn/pages/amacWeb/web-list.html

private product: 私募产品备案信息公示
页面：http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html

私募基金爬取的时候使用到了selenium+PhantomJS
PhantomJS下载地址：http://phantomjs.org/
解压后将bin目录添加到PATH环境变量
（也可以使用ChromeDriver或geckodriver。也需要添加PATH环境变量，另外将privatefund_spider.py中的self.driver改为Chrome或Firefox）