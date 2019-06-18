#!/bin/bash
wrk_dir=`dirname "$0"`
youtube_channel=https://www.youtube.com/channel/UC5X4r8ScZI2AFd_vkjSoytQ
peertube_url=https://peertube.example.com
peertube_user=root
peertube_pwd=super_secret_password_123
CC=True
log=$wrk_dir/data/that_youtube_channel.log

current_dir=`pwd`
cd $wrk_dir
source .env/bin/activate #change '.env' if needed

echo $(date -u) > $log

for t in {1..16} # 4=1hour / 8=2hours / 12=3hours ...
do
    echo "Round $t - " $(date -u) >> $log
    python3 $wrk_dir/yt2pt.py -u $peertube_url -U $peertube_user -p $peertube_pwd -t $youtube_channel -c $CC -q True >> $log
    sleep 900 # wait 15 minutes
done

echo "DONE - " $(date -u) >> $log

cd $current_dir
