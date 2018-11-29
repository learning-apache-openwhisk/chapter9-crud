source _config.mk
export URL="https://$CLOUDANT_USER.cloudant.com"
export AUTH="$CLOUDANT_USER:$CLOUDANT_PASS"

function db {
    op=${1:?method}
    url=${2:?url}
    if test -z "$3"
    then data=""
    else data="-d $3"
    fi
    curl -u $AUTH -X $op $URL/$2 $data
}
