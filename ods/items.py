# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DistributionItem(Item):
    dataset = Field()
    description = Field()
    access_url = Field()

class DatasetItem(Item):
    distributions = Field()
    uri = Field()
    title = Field()
    description = Field()
    issued = Field()
    spatial = Field()
    documentation_title = Field()
    documentation_url = Field()

class OdsSheet(Item):
    datasets = Field()
    xlsx_template = Field()

