from scrapy import Spider

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
