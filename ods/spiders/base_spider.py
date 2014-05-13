###############
## Base spider
##
## The base spider provides a set of defaults on which spiders may want
## to base themselves.

import re
from scrapy.spider import Spider
from scrapy.selector import Selector
from ods.items import OdsSheet, DatasetItem, DistributionItem
from ods.dictionary import country_uri


class OdsSpider( Spider ):
    name = "ebaTable"
    start_urls = [
        "http://www.eba.europa.eu/supervisory-convergence/supervisory-disclosure/aggregate-statistical-data"
    ]
    xlsx_template = "/tmp/template.xlsx"
    
    def parse( self, response ):
        """Parses the EbaSheet available from the response."""
        sheet = OdsSheet()
        sheet['datasets'] = self.parse_datasets( Selector( response ), response )
        sheet['xlsxTemplate'] = self.xlsx_template
        return sheet

    def parse_datasets( self , selector, response ):
        """Parses the datasets from the response."""
        datasets = []
        # for link in selector.xpath('find_datasets'):
        #     dataset = DatasetItem()
        #     item = DistributionItem()
        #     dataset['distributions'] = [item]
        #     dataset["documentationTitle"] = documentationTitle(response)
        #     dataset["documentationUrl"] = documentationUrl(response)
        #     item['description'] = link.xpath('find_description').extract()[0]
        #     item['accessUrl'] = link.xpath('find_access_url').extract()[0]
        #     dataset['title'] = item['description']
        #     dataset['issued'] = link.xpath('find_issued_date').extract()[0]
        #     dataset['spatial'] = link.xpath('find_spatial').extract()[0]
        #     dataset['uri'] = item['accessUrl']
        #     datasets.append(dataset)
        return datasets


class DeclarativeSpider( OdsSpider ):
    """Declarative spider.  Supplying each of the functions fills in the content of the spider."""
    
    ## OVERRIDABLE CONTENT

    # name = String
    # start_urls = [ urls ]
    # xlsx_template = "/tmp/template.xlsx"

    def dataset_finder( self, selector ):
        """Returns the selectors for the datasets found in the document."""
        return []
    def distribution_finder( self, dataset_selector ):
        """Returns the selectors for the distributions found in the document."""
        return [dataset_selector]

    def dataset_issued_date_finder( self, dataset_selector ):
        """Returns the issued date for the dataset."""
        return ""
    def dataset_documentation_title_finder( self, dataset_selector, response ):
        """Returns the documentationTitle for the dataset."""
        return Selector(response).xpath('//title//text()').extract()[0].strip()
    def dataset_documentation_url_finder( self, dataset_selector, response ):
        """Returns the docuentationUrl for the dataset."""
        return response.url
    def dataset_title_finder( self, dataset, dataset_selector ):
        """Returns the title for the dataset."""
        return ""
    def dataset_description_finder( self, dataset, dataset_selector ):
        """Returns the description for the dataset."""
        if len(dataset['distributions'] > 0):
            return dataset['distributions'][0]['description']
        else:
            return ''
    def dataset_uri_finder( self, dataset, dataset_selector ):
        """Returns the uri for the dataset."""
        if len(dataset['distributions']) > 0:
            return dataset['distributions'][0]['accessUrl']
        else:
            return ""
    def dataset_spatial_finder( self, dataset, dataset_selector ):
        """Returns the spatial limitation for the dataset."""
        return ""
    def distribution_description_finder( self, distribution_selector ):
        """Returns the description of the distribution."""
        return ""
    def distribution_access_url_finder( self, distribution_selector ):
        """Returns the description of the distribution."""
        return ""


    ## PLUMBING
    def parse_datasets( self, selector, response ):
        datasets = []
        for datasetSelector in self.dataset_finder( selector ):
            dataset = DatasetItem()
            dataset['documentationTitle'] = self.dataset_documentation_title_finder( datasetSelector, response )
            dataset['documentationUrl' ] = self.dataset_documentation_url_finder( datasetSelector, response )
            dataset['issued'] = self.dataset_issued_date_finder( datasetSelector )
            dataset['distributions'] = self.parse_distributions( datasetSelector )
            dataset['title'] = self.dataset_title_finder( dataset, datasetSelector )
            dataset['uri'] = self.dataset_uri_finder( dataset, datasetSelector )
            datasets.append(dataset)
        return datasets
            
    def parse_distributions( self, datasetSelector ):
        distributions = []
        for distributionSelector in self.distribution_finder( datasetSelector ):
            distribution = DistributionItem()
            distribution['description'] = self.distribution_description_finder( distributionSelector )
            distribution['accessUrl'] = self.distribution_access_url_finder( distributionSelector )
            distributions.append(distribution)
        return distributions
