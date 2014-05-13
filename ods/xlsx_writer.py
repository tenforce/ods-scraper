import os, re, sys, codecs

import shutil, zipfile, os, zipfile

class xlsxfile:
    """Provides support for substituting values in xlsx files"""
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __enter__(self):
        shutil.rmtree('zip', True)
        os.mkdir('zip')
        zipf = zipfile.ZipFile(self.source)
        zipf.extractall('zip')
        return self

    def __exit__(self, type, value, traceback):
        with zipfile.ZipFile(self.target, 'w') as zipf: 
            for root, dirs, files in os.walk("zip"): 
                relroot = os.path.relpath(root, "zip") 
                for file in files: 
                    zipf.write(os.path.join(root, file), os.path.join(relroot, file))
        shutil.rmtree('zip', True)

    def replace(self, original_value, new_value):
        """Replaces the original value with the new value in the xlsx file, 
 assuming it is a simple string."""
        file = "zip/xl/sharedStrings.xml"
        out_fname = file + ".tmp"
        with codecs.open(file, 'r', 'utf-8') as f:
            out = codecs.open(out_fname, 'w', 'utf-8')
            for line in f:
                out.write(line.replace(original_value, new_value))
            out.close()
        os.rename(out_fname, file)
