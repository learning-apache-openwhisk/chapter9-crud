#!/bin/sh
CLOUDANT_USER=${1:?cloudant username}
CLOUDANT_PASS=${2:?cloudant password}

echo "CLOUDANT_USER=$CLOUDANT_USER">_config.mk
echo "CLOUDANT_PASS=$CLOUDANT_PASS">>_config.mk


cat <<EOF >_cloudant.json
{
  "username": "$CLOUDANT_USER",
  "password": "$CLOUDANT_PASS",
  "host": "$CLOUDANT_USER.cloudant.com",
  "port": 443,
  "url": "https://$CLOUDANT_USER:$CLOUDANT_PASS.cloudant.com"
}
EOF

cat <<EOF >init.sh 
$ export CLOUDANT_USER="$CLOUDANT_USER" 
$ export CLOUDANT_PASS="$CLOUDANT_PASS"
$ export URL="https://$CLOUDANT_USER.cloudant.com"
$ export AUTH="$CLOUDANT_USER:$CLOUDANT_PASS"

EOF
