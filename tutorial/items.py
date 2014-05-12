# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DistributionItem(Item):
    dataset = Field()
    description = Field()
    accessUrl = Field()

class DatasetItem(Item):
    title = Field()
    description = Field()
    uri = Field()
    distributions = Field()
    spatial = Field()
    issued = Field()

class EbaSheet(Item):
    datasets = Field()

class Book( Item ):
    title = Field()
    abstract = Field()
