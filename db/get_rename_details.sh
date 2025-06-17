#!/bin/bash

SOURCE=$1
# grep -i "create table" *.sql | sed 's/^.* "/..\/rename_table_from_test.sh / ; s/".*$//; s/Test//'

grep -i "create table" *.sql | sed 's/ *AS *$// ; s/"//g ; s/Test//' | awk -v s=$SOURCE '{printf( "../rename_table_from_test.sh %s %s\n", $NF, s)}'
