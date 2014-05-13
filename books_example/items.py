from scrapy import Item

class Book( Item ):
    title = Field()
    abstract = Field()
