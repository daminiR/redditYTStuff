#!/bin/bash

rootFolderString=$(jq .Inputs[].rootFolder inputs.json)
for var in $rootFolderString
do
    rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$var")
    redditFolder=$rootFolder
    echo $redditFolder
    #python3 ./main/createPDF.py $redditFolder
    #echo converting pdf to png....
    #convert  -flatten -quality 50 -density 144  $redditFolder"/pdf/reddit_single_page.pdf" $redditFolder"/pdf/reddit.png"
    python3 ./main/createScreens.py $redditFolder
done




