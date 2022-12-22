#!/bin/bash

length_inputs=$(jq '.Inputs| length' inputs.json)
rootFolderString=( $(jq .Inputs[].rootFolder inputs.json) )
echo "Enter the text width: "
read text_width
echo "Enter the text width: "
read x_offset

for var_idx in  $(seq $length_inputs);
do
    fontSize=${fontSizeList[var_idx - 1]}
    redditFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"${rootFolderString[var_idx - 1]}")
    echo $redditFolder
    python3 ./main/thumbnail.py $redditFolder $text_width $x_offset
done
