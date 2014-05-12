#!/bin/sh
rm -R csv; mkdir csv
scrapy crawl ebaTable
scrapy crawl ebaStress
scrapy crawl ebaExercise
rm csv.zip
zip -r csv.zip csv
