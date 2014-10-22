# Scrapy settings for value project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'value'

SPIDER_MODULES = ['value.spiders']
NEWSPIDER_MODULE = 'value.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'value (+http://www.yourdomain.com)'
CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 0
DOWNLOAD_TIMEOUT = 180
DOWNLOADER_DEBUG = True
DOWNLOAD_DELAY=1
ITEM_PIPELINES=['value.pipelines.ValuePipeline']

