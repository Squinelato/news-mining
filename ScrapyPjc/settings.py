# -*- coding: utf-8 -*-

BOT_NAME = 'ScrapyPjc'

SPIDER_MODULES = ['ScrapyPjc.spiders']
NEWSPIDER_MODULE = 'ScrapyPjc.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 1.0
AUTOTHROTTLE_ENABLED = True
HTTPCACHE_ENABLED = True



