# Maybe put this in a loop

psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusDropViews.sql 
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusAffiliation.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusAuthor.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusAuthorship.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusPublication.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusSource.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusCitation.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusAuthorKeyword.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusDescriptor.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusCitingViews.sql 

# psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusZipStatus.sql
