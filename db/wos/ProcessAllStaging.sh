# Group into dependencies and do as much in parallel as possible

db_dir=$(dirname $0)
db_script_dir=$db_dir/..

# These can be done indepently
$db_script_dir/ProcessStaging.sh WoSTestGrant \
                                 wos/WoSGrantFromStaging.sql &
grant_generator=$!
$db_script_dir/ProcessStaging.sh WoSTestAffiliation \
                                 wos/WoSAffiliationFromStaging.sql &
affiliation_generator=$!


# This triplet has to finish before anything most else processed
$db_script_dir/ProcessStaging.sh WoSTestAuthor \
                                 wos/WoSAuthorFromStaging.sql 
$db_script_dir/ProcessStaging.sh WoSTestSource  \
                                 wos/WoSSourceFromStaging.sql
$db_script_dir/ProcessStaging.sh WoSTestPublication \
                                 wos/WoSPublicationFromStaging.sql

# These are free agents, but must wait for publications
$db_script_dir/ProcessStaging.sh WoSTestAuthorKeyword \
                                 wos/WoSAuthorKeywordFromStaging.sql &
$db_script_dir/ProcessStaging.sh WoSTestCitation \
                                 wos/WoSCitationFromStaging.sql &
$db_script_dir/ProcessStaging.sh WoSTestPubOrg \
                                 wos/WoSPubOrgFromStaging.sql &
$db_script_dir/ProcessStaging.sh WoSTestPubCountry \
                                 wos/WoSPubCountryFromStaging.sql &
$db_script_dir/ProcessStaging.sh WoSTestPubSubject \
                                 wos/WoSPubSubjectFromStaging.sql &

authorship_with_affiliation_generator=0 

while [ 1 ]
do
  if [ $affiliation_generator -ne 0 ]
  then
    ps -p $affiliation_generator >& /dev/null
    if [ $? -ne 0 ]
    then
      affiliation_generator=0
    fi
  fi

  if [[ affiliation_generator -eq 0 ]]
  then
    $db_script_dir/ProcessStaging.sh WoSTestAuthorshipAffIdStaging \
                                     wos/WoSAuthorshipGetAffiliation.sql
    authorship_with_affiliation_generator=$!
  fi

  if [[ authorship_with_affiliation_generator -ne 0 ]]
  then
    ps -p $authorship_with_affiliation_generator >& /dev/null
    if [ $? -ne 0 ]
    then
      # All prep done
      ( $db_script_dir/ProcessStaging.sh WoSTestAuthorship \
                                     wos/WoSAuthorshipFromStaging.sql) &

      break # The general wait at the end will handle this
    fi
  fi

  if [ $grant_generator -ne 0 ]
  then
    ps -p $grant_generator >& /dev/null
    if [ $? -ne 0 ]
    then
      $db_script_dir/ProcessStaging.sh WoSTestPublicationGrant \
                                     wos/WoSPublicationGrantFromStaging.sql &
      grant_generator=0
    fi
  fi
  sleep 30 # 30" is not long in the scheme of things for this...
done

if [ $grant_generator -ne 0 ]
then
  # This is taking paranoia to new limits

  ps -p $grant_generator >& /dev/null
  if [ $? -ne 0 ]
  then
    # No need to stick in bacground

    $db_script_dir/ProcessStaging.sh WoSTestPublicationGrant \
                                     wos/WoSPublicationGrantFromStaging.sql
  fi
fi

wait 
