#!/bin/sh
rm -R out; mkdir out
for spiderName in {ebaTable,ebaStress,ebaExercise}
do
    scrapy crawl $spiderName
done
rm datasets.zip
zip -r datasets.zip out
