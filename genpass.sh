#!/bin/sh

cp vars.yml-template vars.yml

EXIT=0
while [ $EXIT -eq 0 ]
do
        PASS=$(pwgen -1 64)
        sed -i "0,/PASSWORD/s/PASSWORD/$PASS/" vars.yml
        grep -q PASSWORD vars.yml
        EXIT=$?
done
