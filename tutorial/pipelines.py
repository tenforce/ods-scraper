# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import XmlItemExporter
import os.path
import csv
import csv, codecs, cStringIO

class EbaPipeline(object):

    def process_item(self, ebaSheet, spider):
        """Writes the sheet to a new csv file."""
        # we only have one item to process
        for datasetIndex,dataset in enumerate(ebaSheet.get('datasets',[])):
            filename = os.path.join( "csv", "%s-%s.csv" % (spider.name , datasetIndex) )
            with open( filename , 'w+b' ) as csvfile:
                sheet = UnicodeWriter( csvfile, delimiter=";" )
                ## base dataset metadata
                self.write_dataset_base_metadata( sheet , dataset )
                ## distributions
                self.write_distributions_info( sheet , dataset )
                ## extra dataset metadata
                self.write_dataset_extra_metadata( sheet , dataset )
        return ebaSheet

    def write_dataset_base_metadata( self, sheet, dataset ):
        """Writes the base dataset metadata of the file, this is at the top of the csv."""
        sheet.writerow(["Descriptive metadata"])
        sheet.writerow(["dataset / title_eng", "", "CorporateBodies", dataset.get('title','')])
        sheet.writerow(["dataset / description_eng", "", "", dataset.get('description','')])
        sheet.writerow(["dataset / URI", "", "", dataset.get('uri','')])

    def write_dataset_extra_metadata( self , sheet , dataset ):
        """Adds the extra dataset metadata of the file, this is at the bottom of the csv"""
        sheet.writerow(["dataset / geographical coverage", "", "", dataset.get('spatial','')])
        sheet.writerow(["dataset / issued", "", "", dataset.get('issued','')])
        # - spatial (search for geo)
        # - issued
        
    def write_distributions_info( self , sheet , dataset ):
        """Writes the info about each of the distributions."""
        sheet.writerow([
            "Datasets / distribution",
            """The files containing the data or address of the APIs for accessing it.
            These can be repeated as required for example if the data is being supplied
            in multiple formats, or split into different areas or time periods."""
        ])
        for distribution in dataset.get('distributions',[]):
            self.write_distribution_info( sheet , distribution )
        
    def write_distribution_info( self , sheet , distribution ):
        """Writes the info of a single distribution."""
        sheet.writerow(["dataset / distribution / url", "", "", distribution.get('accessUrl','')])
        sheet.writerow(["dataset / distribution / description", "", "", distribution.get('description','')])

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
