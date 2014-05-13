import re

from scrapy.spider import Spider
from scrapy.selector import Selector

from eba.items import DistributionItem
from eba.items import DatasetItem
from eba.items import Book
from eba.items import EbaSheet
from eba.dictionary import country_uri


#########
# Support
#########

def documentationTitle( response ):
    return Selector(response).xpath('//title//text()').extract()[0].strip()

def documentationUrl( response ):
    return response.url


################
# EbaTableSpider
################

class EbaTableSpider( Spider ):
    name = "ebaTable"
    start_urls = [
        "http://www.eba.europa.eu/supervisory-convergence/supervisory-disclosure/aggregate-statistical-data"
    ]
    
    def parse( self, response ):
        """Parses the EbaSheet available from the response."""
        sheet = EbaSheet()
        sheet['datasets'] = self.parse_datasets( response )
        sheet['xlsxTemplate'] = "/tmp/template.xlsx"
        return sheet

    def parse_datasets( self , response ):
        """Parses the datasets from the response."""
        sel = Selector( response ).xpath('//div[@class="journal-content-article"]')
        datasets = []
        for row in Selector( response ).xpath('//table[@class="Tabular"]//tr[td]'):
            base_title = row.xpath("td[1]//text()").extract()[0].strip()
            for link in row.xpath("td[2]//a"):
                dataset = DatasetItem()
                item = DistributionItem()
                dataset['distributions'] = [item]
                dataset["documentationTitle"] = documentationTitle(response)
                dataset["documentationUrl"] = documentationUrl(response)

                dateArr = link.xpath(".//text()").extract()
                dateLong = "".join( dateArr )
                date = re.sub( ' +', '', dateLong )

                item['description'] = " ".join([base_title , date])
                item['accessUrl'] = "http://www.eba.europa.eu" + link.xpath("@href").extract()[0]

                dataset['title'] = item['description']
                dataset['issued'] = date
                dataset['uri'] = item['accessUrl']

                datasets.append(dataset)
        return datasets

###################
# EbaExerciseSpider
###################

class EbaExerciseSpider( Spider ):
    start_urls = [
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-capital-exercise/final-results",
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2011/results"
    ]
    name="ebaExercise"

    def parse( self, response ):
        sel = Selector( response )
        generalName = sel.xpath('//div[@class="journal-content-article"]//h1/text()').extract()[0].strip()
        rows = sel.xpath('//table[@class="Tabular"]//tr[td]')
        datasets = []
        sheet = EbaSheet()
        sheet['xlsxTemplate'] = "/tmp/template.xlsx"
        for row in rows:
            page_spatial = [ t.strip() for t in row.xpath("td[1]//text()").extract() if re.compile('.*\S.*').match(t) ][0]
            spatial = country_uri( page_spatial )
            for link in row.xpath("td[2]//a"):
                dataset = DatasetItem()
                item = DistributionItem()
                dataset["distributions"] = [item]
                dataset["documentationTitle"] = documentationTitle(response)
                dataset["documentationUrl"] = documentationUrl(response)

                descArr = link.xpath(".//text()").extract()
                descLong = "".join( descArr )
                desc = re.sub( ' +', ' ', descLong )

                item['description'] = desc
                item['accessUrl'] = "http://www.eba.europa.eu" + link.xpath("@href").extract()[0]
        
                dataset['title'] = item['description']
                dataset['spatial'] = spatial
                dataset['uri'] = item['accessUrl']

                datasets.append(dataset)
        sheet['datasets'] = datasets
        return [sheet]


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
        sheet['xlsxTemplate'] = "/tmp/template.xlsx"
        return sheet

    def parse_datasets(self, response):
        """Parses the datasets from the response."""
        datasets = []
        selector = Selector( response )
        for dataset_info in selector.xpath('//div[@class="Timeline"]//dl'):
            dataset = self.parse_dataset(dataset_info)
            dataset['documentationTitle'] = selector.xpath('//title//text()').extract()[0].strip()
            dataset['documentationUrl'] = response.url
            datasets.append( dataset )
        return datasets

    def parse_dataset(self, selector):
        """Create a dataset Item based on a selection."""
        dataset = DatasetItem()
        uris = selector.xpath("dt//a//@href").extract()
        if len(uris) > 0:
            dataset["uri"] =  "http://www.eba.europa.eu" + uris[0]
        else:
            dataset["uri"] = ""
        dataset["title"] = selector.xpath("dt//text()").extract()[0].strip()
        dataset["description"] = ''.join(selector.xpath("dd//text()").extract())
        dataset["issued"] = selector.xpath("dd[@class='TLDate']//text()").extract()[0]
        dataset["distributions"] = self.parse_distribution( selector, dataset.get('uri') )
        return dataset

    def parse_distribution(self, selector, uri):
        distribution = DistributionItem()
        distribution['accessUrl'] =  uri
        distribution['description'] = ''.join(selector.xpath("dd//text()").extract())
        return [distribution]

