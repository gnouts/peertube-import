#!/usr/bin/python3
# pip dependencies: python-dateutil, beautifulsoup4, lxml

from urllib.request import urlopen
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import dateutil.parser as dp 
import xml.etree.ElementTree as ET
import os, sys, errno, time, urllib, subprocess, argparse

# ACCEPT MULTIPLE ANSWER FOR BOOLEAN
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1', 'oui', 'o'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', 'non'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# USAGE and OPTIONS
parser = argparse.ArgumentParser(
    description='Upload videos from a Youtube channel to a Peertube channel, based on RSS feed and license.'
    )
parser.add_argument(
    '-u', 
    metavar='peertube_url',
    dest='PEERTUBE_URL', 
    required=True, 
    help='Peertube url where to upload videos. Example: https://peertube.example.com'
    )
parser.add_argument(
    '-U', 
    '--user', 
    metavar='username', 
    dest='PEERTUBE_USER', 
    required=True, 
    help='Your Peertube username.'
    )
parser.add_argument(
    '-p', 
    '--password', 
    metavar='secretpasswd', 
    dest='PEERTUBE_PASSWORD', 
    required=True, 
    help='Your Peertube user\'s password'
    )
parser.add_argument(
    '-t', 
    '--target', 
    metavar='youtube_url', 
    dest='CHANNEL_URL', 
    required=True, 
    help='Youtube url of the CHANNEL (not the video) to clone. Example: https://www.youtube.com/user/PewDiePie'
    )
parser.add_argument(
    '-c', 
    '--creativecommons', 
    metavar='True', 
    dest='CC_ONLY', 
    type=str2bool, 
    default=True, 
    required=False, 
    help='(Optional) Set to True to upload only videos under Creative Commons license. Set to False to upload all videos no matter licensing. (Default: True)'
    )
parser.add_argument(
    '-l', 
    '--language', 
    metavar='fr', 
    dest='LANGUAGE',
    required=False,
    default='fr',
    help='(Optional) Language tag in the video description. (Default: fr)'
    )
parser.add_argument(
    '-q', 
    '--quiet', 
    metavar='False', 
    dest='QUIET',
    type=str2bool, 
    required=False,
    default=False,
    help='(Optional) Silent output. (Default: False)'
    )
args = parser.parse_args()

# VARIABLES
directory = './data'
ns = {'atom': 'http://www.w3.org/2005/Atom'}
now = datetime.now(timezone.utc)
creativecommons = b'<a href="https://www.youtube.com/t/creative_commons" class=" yt-uix-sessionlink "'
peertube_installation_folder = "PeerTube"  # from git clone
peertube_installation = os.getcwd()+'/'+peertube_installation_folder

try:
    os.makedirs(directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

soup = BeautifulSoup(urlopen(args.CHANNEL_URL), 'lxml')
channelId = soup.find('meta', {'itemprop': 'channelId'})['content']
feed_url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + channelId
path = directory+'/'+channelId+'.txt'
if not(args.QUIET) :
    print('Channel ID: {0}'.format(channelId))
xml_root = ET.parse(urlopen(feed_url)).getroot()

for entry in reversed(xml_root.findall('atom:entry', ns)):
    video_id = entry.find('atom:id', ns).text.split(':')[2]
    published = dp.parse(entry.find('atom:published', ns).text)
    duration = '%d' % (now-published).days
    VIDEO_URL = 'https://www.youtube.com/watch?v=' + video_id
    page = urllib.request.urlopen(VIDEO_URL).read()

    channel_file = open(path,'a+')
    if not video_id in open(path).read():
        if (creativecommons in page):
            if not(args.QUIET) :
                print('Uploading a CC video... ({0})'.format(VIDEO_URL))
            # peertube upload - here
            try:
                subprocess.check_call(['node','dist/server/tools/peertube-import-videos.js','-u',args.PEERTUBE_URL,'-U',args.PEERTUBE_USER,'--password',args.PEERTUBE_PASSWORD,'-t',VIDEO_URL,'-l',args.LANGUAGE],cwd=peertube_installation, timeout=300)
                channel_file.write(video_id+'\n')
            except subprocess.CalledProcessError as e:
                print(e.returncode)
                print(e.cmd)
                print(e.output) 
        elif not args.CC_ONLY and not (creativecommons in page):
            if not(args.QUIET) :
                print('Uploading a non-CC video... ({0})'.format(VIDEO_URL))
            # peertube upload - here
            try:
                subprocess.check_call(['node','dist/server/tools/peertube-import-videos.js','-u',args.PEERTUBE_URL,'-U',args.PEERTUBE_USER,'--password',args.PEERTUBE_PASSWORD,'-t',VIDEO_URL,'-l',args.LANGUAGE],cwd=peertube_installation, timeout=300)
                channel_file.write(video_id+'\n')
            except subprocess.CalledProcessError as e:
                print(e.returncode)
                print(e.cmd)
                print(e.output)
        elif args.CC_ONLY and not (creativecommons in page):
            if not(args.QUIET) :
                print('This video will not be uploaded because of licensing issue : {0}'.format(VIDEO_URL))

    else:
        if not(args.QUIET) :
            print('Already uploaded ({0})'.format(VIDEO_URL))

    channel_file.close()


#####################################
#                                   #
#    Nouts <nouts@protonmail.com>   #
#    January 2019                   #
#                                   #
#####################################

##################################################################################
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                     Version 2, December 2004
#
#  Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
#  Everyone is permitted to copy and distribute verbatim or modified
#  copies of this license document, and changing it is allowed as long
#  as the name is changed.
#
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#   0. You just DO WHAT THE FUCK YOU WANT TO.
#
##################################################################################
