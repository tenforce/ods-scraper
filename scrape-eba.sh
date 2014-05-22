#!/bin/sh
SPIDERS="ebaTable ebaStress ebaExercise"

rm -R out; mkdir out

for spiderName in $SPIDERS
do
    scrapy crawl $spiderName
done

rm datasets.zip
zip -r datasets.zip out
