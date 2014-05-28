from ods.items import OdsSheet, DatasetItem, DistributionItem

from ods.dictionary import country_identifier
from ods.spiders import DeclarativeSpider, OdsSpider


## Use this example spider if you have a simple, well-structured page.  It is easy to use,
## but it has its limitations.  If your page is complex, take a look at MyOdsExampleSpider
## below.
class MyDeclarativeExampleSpider(DeclarativeSpider):
    """Declarative example spider.  Supplying each of the functions fills in the content of your files."""

    # (obligatory) name of your spider
    name = "my-declarative-spider-name"

    # (obligatory) urls which will be scraped
    start_urls = [ "http://my-path/first", "http://my-path/second" ]

    # (optional) override the template to be used for this scraper
    # xlsx_template = "override for template location, eg: /path/to/template.xlsx"

    # (optional) dictionary containing the defaults placed on the sheet of this spider.  these keys
    #            will be prefixed with the standard template prefix key.  the resulting keys are
    #            replaced by the corresponding value.  in this example
    #            __template.tenforce.com/tags would be replaced by "Finance, Eba"
    #            in order to get the replacement working, the key must also appear as a key of
    #            ods.dictionary.defaults_dict
    # sheet_defaults = { 'tags': "Finance, Eba", 'author/name': "eba" }

    # (optional) dictionary containing the prefixes placed on the sheet of this spider.
    # sheet_prefixes = { 'dataset/title': "Title prefix" }

    # (obligatory) executes a selector which returns an array of selectors, selector being a dataset.
    def dataset_finder(self, selector):
        """Returns the selectors for the datasets found in the document."""
        return []

    # (optional) executes a selector which returns an array of distributions, given the selector for a
    #            single dataset.  not supplying this assumes the dataset has a single distribution
    # def distribution_finder(self, dataset_selector):
    #     """Returns the selectors for the distributions found in the document."""
    #     return [dataset_selector]

    # (optional) selects the issued_date given the selector for a dataset.
    # def dataset_issued_date_finder(self, dataset_selector):
    #     """Returns the issued date for the dataset."""
    #     return ""

    # (optional) selects the documentation_title for a dataset, given the dataset's selector 
    #            and the response object.  if this is not supplied, the title of the page is used.
    # def dataset_documentation_title_finder(self, dataset_selector, response):
    #     """Returns the documentation_title for the dataset."""
    #     return Selector(response).xpath('//title//text()').extract()[0].strip()

    # (optional) selects the documentation_url for the dataset given the dataset's selector
    #            and the response object.  if this is not supplied, the response's url is used.
    # def dataset_documentation_url_finder(self, dataset_selector, response):
    #     """Returns the documentation_url for the dataset."""
    #     return response.url

    # (optional) selects the title for the dataset, given the dataset's selector
    # def dataset_title_finder(self, dataset, dataset_selector):
    #     """Returns the title for the dataset."""
    #     return ""

    # (optional) selects the description of the dataset, given the dataset object and the
    #            dataset's selector.  this is executed *after* the distributions have been
    #            discovered and entered.  the default value uses the description of the
    #            first distribution.
    # def dataset_description_finder(self, dataset, dataset_selector):
    #     """Returns the description for the dataset."""
    #     if len(dataset['distributions'] > 0):
    #         return dataset['distributions'][0]['description']
    #     else:
    #         return ''

    # (optional) selects the uri of the dataset, given the dataset object and the dataset's
    #            selector.  this is executed *after*the distributions have been discovered
    #            and rendered.  the default value uses the uri of the first distribution.
    # def dataset_uri_finder(self, dataset, dataset_selector):
    #     """Returns the uri for the dataset."""
    #     if len(dataset['distributions']) > 0:
    #         return dataset['distributions'][0]['access_url']
    #     else:
    #         return ""

    # (optional) selects the spatial coordinate of the dataset, given the distribution's
    #            selector.
    # def dataset_spatial_finder(self, dataset, dataset_selector):
    #     """Returns the spatial limitation for the dataset."""
    #     return ""

    # (optional) selects the description of the distribution, given the distribution's
    #            selector.
    # def distribution_description_finder(self, distribution_selector):
    #     """Returns the description of the distribution."""
    #     return ""

    # (optional) selects th access_url of the distribution, given the distribution's
    #            selector
    # def distribution_access_url_finder(self, distribution_selector):
    #     """Returns the description of the distribution."""
    #     return ""


class  myOdsSpiderExample(OdsSpider):
    """Complex example spider."""

    # (obligatory) name of your spider
    name = "my-declarative-spider-name"

    # (obligatory) urls which will be scraped
    start_urls = [ "http://my-path/first", "http://my-path/second" ]

    # (optional) override the template to be used for this scraper
    # xlsx_template = "override for template location, eg: /path/to/template.xlsx"

    # (optional) dictionary containing the defaults placed on the sheet of this spider.  these keys
    #            will be prefixed with the standard template prefix key.  the resulting keys are
    #            replaced by the corresponding value.  in this example
    #            __template.tenforce.com/tags would be replaced by "Finance, Eba"
    #            in order to get the replacement working, the key must also appear as a key of
    #            ods.dictionary.defaults_dict
    # sheet_defaults = { 'tags': "Finance, Eba", 'author/name': "eba" }

    # (optional) dictionary containing the prefixes placed on the sheet of this spider.
    # sheet_prefixes = { 'dataset/title': "Title prefix" }

    # (obligatory) parse the site and return a series of datasets, based on a Selector
    #              object for the root of the page, and the response object.
    #              This function must return the list of datasets with all their
    #              information filled in.
    #              below is a rough stub body which may be used as a starting point.
    def parse_datasets(self, selector, response):
        """Parses the datasets from the response."""
        datasets = []
        # for link in selector.xpath('find_datasets'):
        #     dataset = DatasetItem()
        #     item = DistributionItem()
        #     dataset.add_distribution(item)
        #     dataset["documentation_title"] = documentation_title(response)
        #     dataset["documentation_url"] = documentation_url(response)
        #     item['description'] = link.xpath('find_description').extract()[0]
        #     item['accessUrl'] = link.xpath('find_access_url').extract()[0]
        #     dataset['title'] = item['description']
        #     dataset['issued'] = link.xpath('find_issued_date').extract()[0]
        #     dataset['spatial'] = link.xpath('find_spatial').extract()[0]
        #     dataset['uri'] = item['accessUrl']
        #     datasets.append(dataset)
        return datasets
