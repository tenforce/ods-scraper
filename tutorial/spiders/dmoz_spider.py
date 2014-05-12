import re

from scrapy.spider import Spider
from scrapy.selector import Selector

from tutorial.items import DistributionItem
from tutorial.items import DatasetItem
from tutorial.items import Book
from tutorial.items import EbaSheet


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
            spatial = [ t.strip() for t in row.xpath("td[1]//text()").extract() if re.compile('.*\S.*').match(t) ][0]
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

############
# BookSpider
############
class BookSpider( Spider ):
    start_urls = [ "http://pastie.org/pastes/9100102/download?key=qks5efkk84bis9igtcut4q" ]
    name = "bookParser"

    def parse( self , response ):
        sel = Selector( response )
        books = []
        for bookTag in sel.xpath('//books/book'):
            book = Book()
            book["title"] = bookTag.xpath('@title').extract()[0]
            book["abstract"] = bookTag.xpath('.//text()').extract()[0].strip()
            books.append( book )
        return books
