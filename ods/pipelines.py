# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import XmlItemExporter
import os.path
from ods.xlsx_writer import xlsxfile
from ods.dictionary import default_dict_keys
from ods.items import get_default, get_prefix

def template_name(path):
    """Return the template identifier based on the relative portion of its name."""
    return "__template.tenforce.com/" + path


class prefixableReplacer:
    """Provides support for replacing values in an object through an xlsxfile, an object to act on and a path and a key in the replacement itself."""
    def __init__(self, xlsx, target):
        self.xlsx = xlsx
        self.target = target

    def replace(self, path, key):
        self.xlsx.replace(template_name(path), self.target.pget(key,path,''))


class OdsPipeline(object):
    """Pipeline which fills in the values in a template xlsx (Microsoft Excel) file"""

    def process_item(self, ods_sheet, spider):
        """Writes the sheet to a new xlsx file."""
        # we only have one item to process
        for dataset_index,dataset in enumerate(ods_sheet.get('datasets', [])):
            target_filename = os.path.join("out", "%s-%s.xlsx" % (spider.name, dataset_index))

            with xlsxfile(ods_sheet.get('xlsx_template'), target_filename) as xlsx:
                ## base dataset metadata
                self.write_dataset_base_metadata(xlsx, dataset)
                ## distributions
                self.write_distributions_info(xlsx, dataset)
                ## extra dataset metadata
                self.write_dataset_extra_metadata(xlsx, dataset)
                ## enter default values
                self.write_default_values(xlsx, dataset)

        return ods_sheet

    def write_dataset_base_metadata(self, xlsx, dataset):
        """Writes the base dataset metadata of the file, this is at the top of the xlsx."""
        template = prefixableReplacer( xlsx, dataset )
        template.replace('dataset/title','title')
        template.replace('dataset/description','description')
        template.replace('dataset/uri','uri')
        template.replace('dataset/documentation/url','documentation_url')
        template.replace('dataset/documentation/title','documentation_title')

    def write_dataset_extra_metadata(self, xlsx, dataset):
        """Adds the extra dataset metadata of the file, this is at the bottom of the xlsx"""
        template = prefixableReplacer( xlsx, dataset )
        template.replace('dataset/geo', 'spatial')
        template.replace('dataset/issued','issued')
        
    def write_distributions_info(self, xlsx, dataset):
        """Writes the info about each of the distributions."""
        distributions = dataset.get('distributions', [])
        row = 1
            
        for distribution in distributions:
            base = template_name("distribution/" + str(row))
            xlsx.replace(base + "/url", distribution.get('access_url', ''))
            xlsx.replace(base + "/description", distribution.get('description', ''))
            row = row + 1

        for r in range(row,30):
            base = template_name("distribution/" + str(r))
            xlsx.replace(base + "/url", "")
            xlsx.replace(base + "/description", "")

    def write_default_values(self, xlsx, dataset):
        """Writes the default values in the xlsx file."""
        for key in default_dict_keys():
            xlsx.replace(template_name(key), get_prefix(key, dataset) + get_default(key, dataset))
