#!/bin/bash

INPUT=mqtt-traffic-055.6.log

API_DESCRIPTIONS="https://raw.githubusercontent.com/goecharger/go-eCharger-API-v2/main/apikeys-de.md https://raw.githubusercontent.com/goecharger/go-eCharger-API-v2/main/apikeys-en.md"
SKIP_KEYS="utc,rbt,loc,dns,ccw,dll"

# https://github.com/goecharger/go-eCharger-API-v2/blob/main/apikeys-de.md
# https://github.com/goecharger/go-eCharger-API-v2/blob/main/apikeys-en.md
# https://github.com/goecharger/go-eCharger-API-v2/blob/main/mqtt-de.md
# https://github.com/goecharger/go-eCharger-API-v2/blob/main/mqtt-en.md

SUPPORTED_BY_FIRMWARE_KEYS=$(cat $INPUT | cut -d" " -f1 | cut -d/ -f4 | sort -u)
SUPPORTED_BY_COMPONENT_KEYS=$(cat ../README.md | grep '^| `' | grep ":heavy_check_mark:" | cut -d\` -f2 | grep -v '+/result' | sort -u)
SUPPORTED_BY_COMPONENT_KEYS_CSV=$(echo $SUPPORTED_BY_COMPONENT_KEYS | sed 's# #,#g' | sed 's#^#,#' | sed 's#$#,#')

API_DESC_DE=$(mktemp)
API_DESC_EN=$(mktemp)

curl -s -o $API_DESC_DE https://raw.githubusercontent.com/goecharger/go-eCharger-API-v2/main/apikeys-de.md
curl -s -o $API_DESC_EN https://raw.githubusercontent.com/goecharger/go-eCharger-API-v2/main/apikeys-en.md

echo "# List of unsupported/new keys"
echo
echo "This script generates a list of unsupported API key by this component but available via MQTT."
echo
echo "List of unsupported but ignored keys: $SKIP_KEYS"
echo

for KEY in $SUPPORTED_BY_FIRMWARE_KEYS;
do
  if echo ",$SKIP_KEYS," | grep -q ",$KEY,"
  then
    continue
  fi

  if ! echo $SUPPORTED_BY_COMPONENT_KEYS_CSV | grep -q ",$KEY,";
  then
    echo "## Key \`$KEY\`"
    echo
    grep $KEY $INPUT | sed 's/^/> /'
    echo
    if ! cat $API_DESC_DE $API_DESC_EN | grep -q "^| ${KEY} "
    then
      echo "No description available"
    else
      echo "| Key        | R/W        | Type                         | Category      | Description                                                                         |"
      echo "| ---------- | ---------- | ---------------------------- | ------------- | ----------------------------------------------------------------------------------- |"
      cat $API_DESC_DE $API_DESC_EN | grep "^| ${KEY} "
    fi
    echo
  fi
done

rm $API_DESC_DE $API_DESC_EN
