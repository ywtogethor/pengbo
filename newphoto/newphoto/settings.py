# Scrapy settings for newphoto project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'newphoto'

SPIDER_MODULES = ['newphoto.spiders']
NEWSPIDER_MODULE = 'newphoto.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'newphoto (+http://www.yourdomain.com)'


CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 0
DOWNLOAD_TIMEOUT = 180
DOWNLOADER_DEBUG = True
#DOWNLOAD_DELAY = 5
DOWNLOAD_DELAY=5 
ITEM_PIPELINES=['newphoto.pipelines.NewphotoPipeline']
