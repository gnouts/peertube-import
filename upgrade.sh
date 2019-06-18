#!/bin/bash

peertube_install_dir=/var/www/peertube

echo '* Loading virtualenv'
source .env/bin/activate

echo '############'
echo '* Upgrading dependencies...'
pip3 install --upgrade python-dateutil beautifulsoup4 lxml youtube-dl --user

echo '############'
echo '* Viewing version'
echo $(node -v)
echo $(yarn -v)
echo $(ffmpeg -version)
echo $(g++ -v)

echo '############'
echo '* Upgrading local PeerTube'
cd PeerTube
git checkout -- .
git checkout master
git fetch --all
git pull --all
version=`grep -Po '\s"version":\s"\K.*(?=")' $peertube_install_dir/package.json`
git_version=v$version
git checkout $git_version
git pull
npm update
yarn install --pure-lockfile
npm run build:server

echo '############'
cd ..
deactivate
source deactivate
echo Done.
