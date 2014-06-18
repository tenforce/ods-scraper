import urlparse

from ods.items import OdsSheet, DatasetItem, DistributionItem
from ods.spiders import OdsSpider

def flat_text(sel):
    """Return the flat text contained in a selector."""
    return " ".join(s.strip() for s in sel.xpath("text()").extract())

class EcfinSurveysSpider(OdsSpider):

    name = "ecfin-surveys"
    start_urls = [ "http://ec.europa.eu/economy_finance/db_indicators/surveys/time_series/index_en.htm" ]

    def parse_datasets(self, selector, response):
        datasets = []
        for link in selector.css(".layout-content table.big_search") \
                            .xpath(".//a[re:test(@href, '\.zip$')]"):
            title = flat_text(link.xpath("ancestor::table[1]//th[1]"))
            target = flat_text(link.xpath("ancestor::tr[1]/td[1]"))
            col = len(link.xpath("ancestor::td[1]/preceding-sibling::td")) + 1
            head = flat_text(link.xpath("ancestor::table[1]//th[%d]" % col))
            dataset = DatasetItem()
            item = DistributionItem()
            dataset.add_distribution(item)
            dataset["documentation_title"] = "Business and Consumer Suveys"
            dataset["documentation_url"] = response.url
            dataset['title'] = " - ".join((title, head, target))
            dataset['uri'] = urlparse.urljoin(response.url, link.xpath("@href").extract()[0])
            item['description'] = dataset['title']
            item['access_url'] = dataset['uri']
            datasets.append(dataset)
        return datasets
