#!/bin/sh
SPIDERS="ebaTable ebaExercise ebaStress2011"

rm -R out; mkdir out

for spiderName in $SPIDERS
do
    scrapy crawl $spiderName
done

rm datasets.zip
zip -r datasets.zip out
