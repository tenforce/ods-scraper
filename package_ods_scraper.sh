#!/bin/sh
echo "Packaging ods scraper $1 in ../ods_scraper_$1"

NEW_BASE="../ods_scraper_$1"

if [ -d $NEW_BASE ]
then
    echo "Directory $NEW_BASE already exists, please remove it if you want to rebuild release $1"
else
    ## make folder structure
    echo -n "Making folder structure... "
    mkdir $NEW_BASE
    for line in `find ./ -mindepth 1 -not -ipath "*.git*" -not -iname "*.pyc" -not -iname "*~" -not -ipath "*/out/*" -type d`
    do
        mkdir $NEW_BASE/$line
    done
    echo "DONE"

    ## copy files
    echo -n "Copying files... "
    for line in `find ./ -not -ipath "*.git*" -not -iname "*.pyc" -not -iname "*~" -not -ipath "*/out/*" -type f`
    do
        cp $line $NEW_BASE/$line
    done
    echo "DONE"

    echo "Your new ODS Scraper build is available in $NEW_BASE"
fi
