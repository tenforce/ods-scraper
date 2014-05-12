import re

from scrapy.spider import Spider
from scrapy.selector import Selector

from tutorial.items import DistributionItem
from tutorial.items import DatasetItem
from tutorial.items import EbaSheet

#################
# EbaStressSpider
#################

class EbaStressSpider( Spider ):
    start_urls = [
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2009",
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2010",
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2011",
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2014"
    ]
    name = "ebaStress"

    def parse( self, response ):
        """Parses the EbaSheet available from the response."""
        sheet = EbaSheet()
        sheet['datasets'] = self.parse_datasets( response )
        return sheet

    def parse_datasets(self, response):
        """Parses the datasets from the response."""
        datasets = []
        for dataset_info in Selector ( response ).xpath('//div[@class="Timeline"]//dl'):
            datasets.append( self.parse_dataset(dataset_info) )
        return datasets

    def parse_dataset(self, selector):
        """Create a dataset Item based on a selection."""
        dataset = DatasetItem()
        uris = selector.xpath("dt//a//@href").extract()
        if len(uris) > 0:
            dataset["uri"] =  "http://www.eba.europa.eu" + uris[0]
        dataset["title"] = selector.xpath("dt//text()").extract()[0].strip()
        dataset["description"] = ''.join(selector.xpath("dd//text()").extract())
        dataset["issued"] = selector.xpath("dd[@class='TLDate']//text()").extract()[0]
        dataset["distributions"] = self.parse_distribution( selector, dataset['uri'] )
        return dataset

    def parse_distribution(self, selector, uri):
        distribution = DistributionItem()
        distribution['accessUrl'] =  uri
        distribution['description'] = ''.join(selector.xpath("dd//text()").extract())
        return [distribution]

