aws polly start-speech-synthesis-task \
  --region us-east-1 \
  --endpoint-url "https://polly.us-east-1.amazonaws.com/" \
  --output-format mp3 \
  --output-s3-bucket-name reddityoutube2 \
  --voice-id Matthew \
  --engine "neural" \
  --text file:../OCt_30_2022/reddit_yt_2/reddit_1.xml \


