# Scrapy settings for kimiss project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kimiss'

SPIDER_MODULES = ['kimiss.spiders']
NEWSPIDER_MODULE = 'kimiss.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kimiss (+http://www.yourdomain.com)'
CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 15
CONCURRENT_REQUESTS_PER_DOMAIN = 15
CONCURRENT_REQUESTS_PER_IP = 0
DOWNLOAD_TIMEOUT = 180
DOWNLOADER_DEBUG = True
DOWNLOAD_DELAY=0
ITEM_PIPELINES=['kimiss.pipelines.KimissPipeline']

