import os, re, sys, codecs

class xlsxfile:
    def __init__(self, source, target):
        self.source = source
        self.target = target
    def __enter__(self):
        os.system('rm -Rf zip; mkdir zip')
        os.system("unzip " + self.source + " -d zip")
        return self
    def __exit__(self, type, value, traceback):
        os.system('cd zip; zip -r ' + '../' + self.target + ' *; rm -R ../zip')
    def replace(self, original_value, new_value):
        # print "Replacing " + original_value + " with " + new_value
        file = "zip/xl/sharedStrings.xml"
        out_fname = file + ".tmp"
        with codecs.open(file, 'r', 'utf-8') as f:
            out = codecs.open(out_fname, 'w', 'utf-8')
            for line in f:
                out.write( line.replace(original_value, new_value) )
            out.close()
        os.rename(out_fname, file)
