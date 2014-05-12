#!/bin/sh
rm -R out; mkdir out
scrapy crawl ebaTable
scrapy crawl ebaStress
scrapy crawl ebaExercise
rm datasets.zip
zip -r datasets.zip out
