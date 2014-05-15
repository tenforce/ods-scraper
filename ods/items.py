# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from ods.dictionary import get_dictionary_default

def get_default(path, target):
    """Retrieves the default value for the supplied path.  eg: /datasets/publisher"""
    current_item_defaults = target['defaults']

    if path in current_item_defaults:
        return current_item_defaults[path]
    elif isinstance(target['wrapper'], ItemWithDefaults):
        return get_default(path, target['wrapper'])
    else:
        return get_dictionary_default(path)


class ItemWithDefaults(Item):
    defaults = Field()
    wrapper = Field()
    
    def __init__(self, *args, **kw):
        super(ItemWithDefaults, self).__init__(*args, **kw)
        self['defaults'] = {}
        self['wrapper'] = None

    def set_default(self, path, value):
        """Sets the default value for path to value."""
        self['defaults'][path] = value

    def set_wrapper(self, value):
        """Sets the item's wrapper"""
        self['wrapper'] = value

    def import_defaults(self, defaults):
        """Imports a dictionary of defaults."""
        for key in defaults.keys():
            self.set_default(key, defaults[key])


class DistributionItem(Item):
    dataset = Field()
    description = Field()
    access_url = Field()

    def __str__(self):
        return "DistributionItem(access_url=%s)" % self['access_url']

class DatasetItem(ItemWithDefaults):
    distributions = Field()
    uri = Field()
    title = Field()
    description = Field()
    issued = Field()
    spatial = Field()
    documentation_title = Field()
    documentation_url = Field()

    def __init__( self, *args, **kw):
        super(DatasetItem, self).__init__(*args, **kw)
        self['distributions'] = []

    def __str__(self):
        return "DatasetItem(uri=%s)" % self['uri']

    def add_distribution(self, distribution):
        """Adds a single distribution to the dataset."""
        self['distributions'].append(distribution)

    def add_distributions(self, distributions):
        """Adds an array of distributions to the dataset."""
        for distribution in distributions:
            self.add_distribution(distribution)

class OdsSheet(ItemWithDefaults):
    datasets = Field()
    xlsx_template = Field()
    
    def __init__(self, *args, **kw):
        super(OdsSheet, self).__init__(*args, **kw)
        self['datasets'] = []

    def __str__(self):
        return "OdsSheet()"

    def add_dataset(self, dataset):
        """Adds a single dataset to the sheet."""
        dataset.set_wrapper(self)
        self['datasets'].append(dataset)

    def add_datasets(self, datasets):
        """Adds an array of datasets to the sheet."""
        for dataset in datasets:
            self.add_dataset(dataset)
