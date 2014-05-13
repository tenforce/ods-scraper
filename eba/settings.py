# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html

BOT_NAME = 'tf-ebabottle'

SPIDER_MODULES = ['eba.spiders']
NEWSPIDER_MODULE = 'eba.spiders'

ITEM_PIPELINES = {
    "eba.pipelines.EbaPipeline": 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'eba (+http://www.yourdomain.com)'
