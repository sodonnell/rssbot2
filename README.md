# rssbot2

A modern version of my ancient rssbot module, written in python3.

**Table of Contents:**
- [rssbot2](#rssbot2)
- [Overview](#Overview)
  - [rssbot vs rssbot2](#rssbot-vs-rssbot2)
  - [RSS Reader Interface development](#RSS-Reader-Interface-development)
  - [RSS is Dead, though, so why bother?](#RSS-is-Dead-though-so-why-bother)
- [Requirements](#Requirements)
- [Installation](#Installation)
- [Usage Examples](#Usage-Examples)
  - [crontab](#crontab)
  - [django integration](#django-integration)
  - [one-off commands/scripts](#one-off-commandsscripts)

# Overview

The rssbot2 python script is intended to monitor a random list of RSS Feeds that are defined within a mysql database table, on a continuous basis, and gather/add any new articles that have been published since the last monitoring session.

## rssbot vs rssbot2

My original rssbot script was written back in 2007, and used python 2.4 (at the time), as well as the old/deprecated MySQLdb library to interact with a mysql database.

This rssbot2 script is written in python 3.6, and uses the MySQL Connector library to interact with mysql. 
https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html

The other main difference between rssbot and rssbot2 is that now in python3 (or more accurately, since python 2.7), unicode support has been fixed to better handle character sets that otherwise would choke my old rssbot script, or cause unicode parsing exceptions, which was very frustrating back in 2007.

## RSS Reader Interface development

This allows for the development of a web interface that displays the latest links/articles from an archive of registered RSS feeds. Essentially, you can create an interface to view the latest content to hit the web from all of your favorite web sites that support RSS Syndication.

## RSS is Dead, though, so why bother?

While some/most consider RSS to be a DOA technology in 2019, the fact remains that there are still hundreds of thousands of web sites that still support syndication via RSS/ATOM format. 

# Requirements

* Python >= 3.6
* feedparser
* mysql-connector-python

```
pip3 install feedparser mysql-connector-python
```

# Installation

It's pretty straight-forward.

1) Clone this repo.
2) Make setup.py executable.
3) Run the setup.py script.
4) Enter the database configuration information during the setup process.

```
git clone https://github.com/sodonnell/rssbot2.git
cd rssbot2
chmod +x setup.py
./setup.py
```

# Usage Examples

## crontab

## django integration

## one-off commands/scripts

The add_feed.py script is an interactive shell script that will prompt you to fill-in the blanks.

```
./add_feed.py
```

It will ask you to provide the RSS url, and whether or not the feed should be active. Eventually, this interactivity will be optionally supressed by command-line arguments.
