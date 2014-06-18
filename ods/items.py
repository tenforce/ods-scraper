# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from ods.dictionary import get_dictionary_default, get_default_prefix

def get_default(path, target):
    """Retrieves the default value for the supplied path (eg: /datasets/publisher).  Bubbling up from target."""
    current_item_defaults = target['defaults']
    if path in current_item_defaults:
        return current_item_defaults[path]
    elif isinstance(target['wrapper'], OdsExtendedItem):
        return get_default(path, target['wrapper'])
    else:
        return get_dictionary_default(path)

def get_prefix(path, target):
    """Retrieves the default value for the supplied path (eg: /datasets/publisher).  Bubbling up from target."""
    current_item_prefixes = target['prefixes']
    if path in current_item_prefixes:
        return current_item_prefixes[path]
    elif isinstance(target['wrapper'], OdsExtendedItem):
        return get_prefix(path, target['wrapper'])
    else:
        return get_default_prefix(path)


class OdsExtendedItem(Item):
    """Wrapped item with support for defaults and prefixes."""
    defaults = Field()
    wrapper = Field()
    prefixes = Field()
    
    def __init__(self, *args, **kw):
        super(OdsExtendedItem, self).__init__(*args, **kw)
        self['defaults'] = {}
        self['prefixes'] = {}
        self['wrapper'] = None

    def set_default(self, path, value):
        """Sets the default value for path to value."""
        self['defaults'][path] = value

    def set_prefix(self, path, value):
        """Sets the prefix for path to value."""
        self['prefixes'][path] = value

    def set_wrapper(self, value):
        """Sets the item's wrapper"""
        self['wrapper'] = value

    def import_defaults(self, defaults):
        """Imports a dictionary of defaults."""
        for key in defaults.keys():
            self.set_default(key, defaults[key])

    def import_prefixes(self, prefixes):
        """Imports a dictionary of prefixes."""
        for key in prefixes.keys():
            self.set_prefix(key, prefixes[key])
    
    def pget(self, key, path, default):
        """Prefixed version of get.  The prefix is only applied if the value had been set."""
        if key in self:
            return get_prefix(path, self) + self.get(key)
        else:
            return default


class DistributionItem(Item):
    dataset = Field()
    description = Field()
    access_url = Field()
    distribution_type = Field()

    def __str__(self):
        return "DistributionItem(access_url=%s)" % self['access_url']

class DatasetItem(OdsExtendedItem):
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

    def ckan_name(self):
        """Returns the ckan-name, which is a name based on the title"""
        return self.get('title','').replace(' ','_')

    def add_distribution(self, distribution):
        """Adds a single distribution to the dataset."""
        self['distributions'].append(distribution)

    def add_distributions(self, distributions):
        """Adds an array of distributions to the dataset."""
        for distribution in distributions:
            self.add_distribution(distribution)

class OdsSheet(OdsExtendedItem):
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
