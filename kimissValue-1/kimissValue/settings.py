# Scrapy settings for kimissValue project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kimissValue'

SPIDER_MODULES = ['kimissValue.spiders']
NEWSPIDER_MODULE = 'kimissValue.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kimissValue (+http://www.yourdomain.com)'

CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 5
CONCURRENT_REQUESTS_PER_IP = 0
DOWNLOAD_TIMEOUT = 180
DOWNLOADER_DEBUG = True
DOWNLOAD_DELAY=0
ITEM_PIPELINES=['kimissValue.pipelines.KimissvaluePipeline']
