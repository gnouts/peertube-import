! Ce dépôt est un clone utilisé pour la visibilité et les issues.

! Pour le code le plus à jour, voir le projet : https://taboulisme.com/git/nouts/peertube-import/

# Import de video youtube automatique, basé sur le flux rss d'une chaîne
[English ReadMe](README-en.md)

Le script liste les url des videos d'une channel et les importe dans peertube.

La trace des vidéos importées est enregistrée dans des fichiers textes. No database yet...

A utiliser avec cron, par exemple (voir cronify.sh).

Ce script est basé sur [ce POC](https://framagit.org/snippets/1891). ([ref](https://github.com/Chocobozzz/PeerTube/issues/754))

## Installation

### Installation des dépendances du script

Le script ne fonctionne que sous *Python3*.

Téléchargez/Clonez ce dépôt, puis :
```
cd peertube-import
pip install virtualenv
virtualenv .env
source .env/bin/activate
pip install python-dateutil beautifulsoup4 lxml
``` 

### Installation de PeerTube

Il est nécessaire de build les sources de PeerTube pour pouvoir utiliser les scripts d'import, même si vous avez déjà une installation de PeerTube en locale. (cf. [doc](https://github.com/Chocobozzz/PeerTube/blob/develop/support/doc/tools.md#remote-tools))

Vous aurez besoin de [NodeJS](https://nodejs.org/en/download/package-manager) et [Yarn](https://yarnpkg.com/en/docs/install#debian-stable), ainsi que :

``` 
sudo apt-get install curl unzip vim ffmpeg openssl g++ make git
```

Vérifiez les versions
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

Clonez PeerTube pour avoir accès aux script d'import.js :
```
git clone https://github.com/Chocobozzz/PeerTube.git

```
Lancez le script *upgrade.sh*. Il va s'occuper de retrouver la version de votre 'vraie' installation PeerTube, se positioner sur le bon tag et compiler les sources.

Il vous faut modifier dans l'en-tête le dossier d'installation de votre 'vraie' PeerTube.

Si le script ne fonctionne pas, vous pouvez simplement exécuter les commandes suivantes :
```
cd PeerTube
# changez le tag/branch suivant la version actuelle/souhaitée de PeerTube
git checkout v1.3.0
yarn install --pure-lockfile
npm run build:server
```

Fini ! :)

Vous pouvez maintenant lancer le programme yt2pt.py.

Personnellement, j'exécute le programme via un script appelé tous les soirs (à l'heure où mes youtubeurs publient statistiquement leur vidéo) via crontab.

Un exemple de ce script se trouve dans *cronify.sh*. (Il charge l'environnement Python et lance le programme dans une boucle, 8 fois à 15 minutes d'intervalle. Ce qui permet de détecter les nouvelles vidéos pendant 2 heures. A adapter suivant les besoins/ressources.)

## Note

### fr

L'import des vidéos se fait dans l'ordre chronologique (ordre inverse du flux RSS).

Par défaut, le flux RSS fournit par YouTube ne retourne que 14 vidéos. (Je n'ai pas cherché à aller plus loin) 

Au premier lancement, il n'y aura donc qu'au maximum 14 vidéos. (Aussi, si le script ne tourne pas assez souvent et que beaucoup de vidéos sont uploadées sur YouTube, il est possible que le script en loupe)

## Usage

Le flux RSS de Youtube ne fournit que 14 vidéos. Au premier lancement le script n'importera donc que 14 vidéos (au mieux, suivant les licences).

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

