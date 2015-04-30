# Scrapy settings for tmall_list project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tmall_list'

SPIDER_MODULES = ['tmall_list.spiders']
NEWSPIDER_MODULE = 'tmall_list.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tmall_list (+http://www.yourdomain.com)'

CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 0
DOWNLOAD_TIMEOUT = 180
DOWNLOADER_DEBUG = True
DOWNLOAD_DELAY=0
ITEM_PIPELINES=['tmall_list.pipelines.TmallListPipeline']
LOG_LEVEL = "WARNING"
LOG_FILE = "tmall_list.log"


