#!/bin/bash

length_inputs=$(jq '.Inputs| length' inputs.json)
rootFolderString=( $(jq .Inputs[].rootFolder inputs.json) )

for var_idx in  $(seq $length_inputs);
do
    fontSize=${fontSizeList[var_idx - 1]}
    redditFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"${rootFolderString[var_idx - 1]}")
    echo $redditFolder
    python3 ./main/thumbnail.py $redditFolder
done
