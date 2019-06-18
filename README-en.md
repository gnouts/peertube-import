# Import youtube videos automamagically, from a Youtube channel's rss feed
[French ReadMe](README.md)

This script list videos url from a channel and import them in peertube.

The imported video history is stored in plain text files. No database yet...

It's mean to use with a cron job, see *cronify.sh* for example.

This script is based on [this POC.](https://framagit.org/snippets/1891). ([ref](https://github.com/Chocobozzz/PeerTube/issues/754))

## Installation

### Installating dependencies

This script requires *Python3*.

Download/Clone this repository, then :
```
cd peertube-import
pip install virtualenv
virtualenv .env
source .env/bin/activate
pip install python-dateutil beautifulsoup4 lxml
``` 

### Installating PeerTube

You need to build a local Peertube to use peertube's own import scripts, even if you already have a working PeerTube instance running on the same machine. (see [official doc](https://github.com/Chocobozzz/PeerTube/blob/develop/support/doc/tools.md#remote-tools))

You'll need [NodeJS](https://nodejs.org/en/download/package-manager) and [Yarn](https://yarnpkg.com/en/docs/install#debian-stable), and :

``` 
sudo apt-get install curl unzip vim ffmpeg openssl g++ make git
```

Verify dependencies version :
```
# Should be >= 8.x
node -v

# Should be >= 1.5.1
yarn -v

# Should be >= 3.x
ffmpeg -version

# Should be >= 5.x
g++ -v
```

Clone Peertube to access its import.js scripts :
```
git clone https://github.com/Chocobozzz/PeerTube.git

```
Then, you can run *upgrade.sh*. It'll retrieve your running Peertube version, checkout the proper tag so both Peertube version match, and compile it.

You'll have to modify the variable header to provide the installation directory of your running Peertube. (So *upgrade.sh* works only if PeerTube is running on the same machine.)

If the *upgrade.sh* does not suit you, you can simply run that :
```
cd PeerTube
# change the tag/branch to match your needs
git checkout v1.3.0
yarn install --pure-lockfile
npm run build:server
```

Done ! :)

Now, you can run yt2pt.py.

FIY, I run this program through a script every evenings via crontab (when the youtubers I care about upload their videos, statistically)

A script example is avaible in *cronify.sh*. (it loads the python env, and run the program in a loop, 8 times with 15 minutes interval. This way it detects all new uploaded videos during 2 hours. Adapt to suit your needs)


## Note

Videos are imported in chronological order (reverse from the rss feed).

By default, Youtube's RSS feed only returns 14 videos. (I didn't look more indepth)

At first run, there will only be 14 videos uploaded. (Also, if the script isn't run too often and lots of videos are uploaded on YouTube, it might miss some).

## Usage

The RSS feed from Youtube only provides 14 videos. At first run it will only import the 14 last videos from the channel.

```
> cd peertube-import
> source .env/bin/activate
> python3 yt2pt.py -h
usage: yt2pt.py [-h] -u peertube_url -U username -p secretpasswd -t
                youtube_url [-c True] [-l fr] [-q False]

Upload videos from a Youtube channel to a Peertube channel, based on RSS feed.

optional arguments:
  -h, --help            show this help message and exit
  -u peertube_url       Peertube url where to upload videos.
                        Example:https://peertube.example.com
  -U, --user username
                        Your Peertube username.
  -p, --password secretpasswd
                        Your Peertube user's password.
  -t, --target youtube_url
                        Youtube url of the CHANNEL (not the video) to clone.
                        Example: https://www.youtube.com/user/PewDiePie
  -c, --creativecommons True
                        (Optional) Set to True to upload only videos under
                        Creative Commons license. Set to False to upload all
                        videos no matter licensing. (Default: True)
  -l, --language fr     (Optional) Language tag in the video description. (Default: fr)
  -q, --quiet False
                        (Optional) Silent output. (Default: False)

``` 



# License

                                   
    Nouts <nouts@protonmail.com>   
    January 2019                   


    DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
    Version 2, December 2004

    Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

    Everyone is permitted to copy and distribute verbatim or modified
    copies of this license document, and changing it is allowed as long
    as the name is changed.

    DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

    0. You just DO WHAT THE FUCK YOU WANT TO.

