import re

from urlparse import urlparse

from scrapy.spider import Spider
from scrapy.selector import Selector

from ods.items import OdsSheet, DatasetItem, DistributionItem
from ods.dictionary import country_identifier
from ods.spiders import DeclarativeSpider, OdsSpider


#########
# Support
#########

def documentation_title(response):
    return Selector(response).xpath('//title//text()').extract()[0].strip()

def documentation_url(response):
    return response.url


################
# EbaTableSpider
################

class EbaTableSpider(OdsSpider):
    name = "ebaTable"
    start_urls = [
        "http://www.eba.europa.eu/supervisory-convergence/supervisory-disclosure/aggregate-statistical-data"
    ]

    sheet_defaults = {'sheet/spider': 'EbaTableSpider'}
    sheet_prefixes = {'dataset/title': 'Dataset title prefix: '}
    
    def parse_datasets(self , selector, response):
        """Parses the datasets from the response."""
        datasets = []
        for row in selector.xpath('//table[@class="Tabular"]//tr[td]'):
            base_title = row.xpath("td[1]//text()").extract()[0].strip()
            for link in row.xpath("td[2]//a"):
                dataset = DatasetItem()
                dataset.set_default('dataset/base_title', base_title)
                item = DistributionItem()
                dataset.add_distribution(item)
                dataset["documentation_title"] = documentation_title(response)
                dataset["documentation_url"] = documentation_url(response)

                date_arr = link.xpath(".//text()").extract()
                date_long = "".join( date_arr )
                date = re.sub( ' +', '', date_long )

                item['description'] = " ".join([base_title , date])
                item['access_url'] = urlparse.urljoin("http://www.eba.europa.eu", link.xpath("@href").extract()[0])

                dataset['title'] = item['description']
                dataset['issued'] = date
                dataset['uri'] = item['access_url']

                datasets.append(dataset)
        return datasets

###################
# EbaExerciseSpider
###################

class EbaExerciseSpider(Spider):
    """Parses the eu capital exercise.  This extends Spider instead of OdsSpider and provides a manual example."""
    start_urls = [
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-capital-exercise/final-results",
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2011/results"
    ]
    name="ebaExercise"

    def parse(self, response):
        sel = Selector(response)
        generalName = sel.xpath('//div[@class="journal-content-article"]//h1/text()').extract()[0].strip()
        rows = sel.xpath('//table[@class="Tabular"]//tr[td]')
        datasets = []
        sheet = OdsSheet()
        sheet['xlsx_template'] = "template.xlsx"
        for row in rows:
            page_spatial = [t.strip() for t in row.xpath("td[1]//text()").extract() if re.match(r’.*\S.*’, t)][0]
            spatial = country_identifier(page_spatial)
            for link in row.xpath("td[2]//a"):
                dataset = DatasetItem()
                item = DistributionItem()
                dataset["distributions"] = [item]
                dataset["documentation_title"] = documentation_title(response)
                dataset["documentation_url"] = documentation_url(response)

                descArr = link.xpath(".//text()").extract()
                descLong = "".join(descArr)
                desc = re.sub(' +', ' ', descLong)

                item['description'] = desc
                item['access_url'] = urlparse.urljoin("http://www.eba.europa.eu", link.xpath("@href").extract()[0])
        
                dataset['title'] = item['description']
                dataset['spatial'] = spatial
                dataset['uri'] = item['access_url']

                datasets.append(dataset)
        sheet['datasets'] = datasets
        return [sheet]


#################
# EbaStressSpider
#################

class EbaStressSpider(OdsSpider):
    name = "ebaStress"

    start_urls = [
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2009",
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2010",
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2011",
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2014"
    ]

    def parse_datasets(self, selector, response):
        """Parses the datasets from the response."""
        datasets = []
        for dataset_info in selector.xpath('//div[@class="Timeline"]//dl'):
            dataset = self.parse_dataset(dataset_info)
            dataset['documentation_title'] = selector.xpath('//title//text()').extract()[0].strip()
            dataset['documentation_url'] = response.url
            datasets.append(dataset)
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
        distribution['access_url'] =  uri
        distribution['description'] = ''.join(selector.xpath("dd//text()").extract())
        return [distribution]


class DeclarativeEbaStressSpider(DeclarativeSpider):
    name = "declarativeEbaStress"

    start_urls = [
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2009",
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2010",
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2011",
        "http://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing/2014"
    ]
    
    def dataset_finder(self, selector):
        return selector.xpath('//div[@class="Timeline"]//dl')

    def dataset_issued_date_finder(self, selector):
        return selector.xpath("dd[@class='TLDate']//text()").extract()[0]
        
    def dataset_title_finder(self, dataset, selector):
        return selector.xpath("dt//text()").extract()[0].strip()

    def distribution_description_finder(self, selector):
        return ''.join(selector.xpath("dd//text()").extract())
        
    def distribution_access_url_finder(self, selector):
        uris = selector.xpath("dt//a//@href").extract()
        if len(uris) > 0:
            return "http://www.eba.europa.eu" + uris[0]
        else:
            return ""
