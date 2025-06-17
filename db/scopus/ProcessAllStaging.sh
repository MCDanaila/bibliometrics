# Maybe put this in a loop

date # During dev
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusAffiliationFromStaging.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusSourceFromStaging.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusAuthorFromStaging.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusAuthorshipGetAffiliation.sql
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f `dirname $0`/ScopusAuthorshipFromStaging.sql
date # During dev
