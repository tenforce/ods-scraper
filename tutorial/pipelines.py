# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import XmlItemExporter
import os.path
import csv
import csv, codecs, cStringIO
from tutorial.xlsx_writer import xlsxfile

def template_name( path ):
    return "__template.tenforce.com/" + path

class EbaPipeline(object):

    def process_item(self, ebaSheet, spider):
        """Writes the sheet to a new xlsx file."""
        # we only have one item to process
        for datasetIndex,dataset in enumerate(ebaSheet.get('datasets',[])):
            target_filename = os.path.join( "out", "%s-%s.xlsx" % (spider.name , datasetIndex) )

            with xlsxfile( ebaSheet.get('xlsxTemplate') , target_filename ) as xlsx:
                ## base dataset metadata
                self.write_dataset_base_metadata( xlsx , dataset )
                ## distributions
                self.write_distributions_info( xlsx , dataset )
                ## extra dataset metadata
                self.write_dataset_extra_metadata( xlsx , dataset )

        return ebaSheet

    def write_dataset_base_metadata( self, xlsx, dataset ):
        """Writes the base dataset metadata of the file, this is at the top of the xlsx."""
        xlsx.replace(template_name('dataset/title'), dataset.get('title',''))
        xlsx.replace(template_name('dataset/description'), dataset.get('description',''))
        xlsx.replace(template_name('dataset/uri'), dataset.get('uri',''))
        xlsx.replace(template_name('dataset/documentation/url'), dataset.get('documentationUrl',''))
        xlsx.replace(template_name('dataset/documentation/title'), dataset.get('documentationTitle',''))

    def write_dataset_extra_metadata( self , xlsx , dataset ):
        """Adds the extra dataset metadata of the file, this is at the bottom of the xlsx"""
        xlsx.replace(template_name('dataset/geo'), dataset.get('spatial',''))
        xlsx.replace(template_name('dataset/issued'), dataset.get('issued',''))
        
    def write_distributions_info( self , xlsx , dataset ):
        """Writes the info about each of the distributions."""
        distributions = dataset.get('distributions', [])
        row = 1
        for distribution in distributions:
            base = template_name("distribution/" + str(row))
            xlsx.replace(base + "/url", distribution.get('accessUrl',''))
            xlsx.replace(base + "/description", distribution.get('description',''))
            row = row + 1
        for r in range(row,30):
            base = template_name("distribution/" + str(r))
            xlsx.replace(base + "/url", "")
            xlsx.replace(base + "/description", "")
