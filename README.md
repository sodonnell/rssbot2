# rssbot2 <!-- omit in toc -->

A modern version of my ancient rssbot module, written in python3.

**Table of Contents:**
- [Overview](#Overview)
  - [rssbot vs rssbot2](#rssbot-vs-rssbot2)
  - [RSS Reader Interface development](#RSS-Reader-Interface-development)
  - [RSS is Dead, though, so why bother?](#RSS-is-Dead-though-so-why-bother)
- [Requirements](#Requirements)
- [Installation](#Installation)
- [Script Usage](#Script-Usage)
  - [add_feed.py](#addfeedpy)
  - [runner.py](#runnerpy)
- [Automation via cron](#Automation-via-cron)
  - [crontab interval](#crontab-interval)
    - [Small RSS Feed Inventory](#Small-RSS-Feed-Inventory)
    - [Large RSS Feed Inventory](#Large-RSS-Feed-Inventory)
    - [Personal Blogs](#Personal-Blogs)
    - [Mainstream News/Blogs](#Mainstream-NewsBlogs)
- [Python Framework Integration](#Python-Framework-Integration)
  - [Django](#Django)
  - [Flask](#Flask)

# Overview

The rssbot2 python script is intended to monitor a random list of RSS Feeds that are defined within a mysql database table, on a continuous basis, and gather/add any new articles (links) that have been published since the last monitoring session.

## rssbot vs rssbot2

My original rssbot script was written back in 2007, and used python 2.4 (at the time), as well as the old/deprecated MySQLdb library to interact with a mysql database.

This rssbot2 script is written in python 3.6, and uses the MySQL Connector library to interact with mysql. 
https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html

The other main difference between rssbot and rssbot2 is that now in python3 (or more accurately, since python 2.7), unicode support has been fixed to better handle character sets that otherwise would choke my old rssbot script, or cause unicode parsing exceptions, which was very frustrating back in 2007.

## RSS Reader Interface development

This project allows for the development of a web interface that displays the latest links/articles from an archive of registered RSS feeds. Essentially, you can create an interface to view the latest content to hit the web from all of your favorite web sites that support RSS Syndication.

This project does not include an integrated RSS Reader Interface, but it does allow you to build your own based upon whatever Web/Mobile development language or framework you choose, such as Node.js, PHP, Python, Ruby, etc.

The scope of this script is purely for the back-end automation of collecting, parsing and ingesting RSS Data into a MySQL Database.

## RSS is Dead, though, so why bother?

While some/most consider RSS to be a DOA technology in 2019, the fact remains that there are still hundreds of thousands of web sites that still support syndication via RSS/ATOM format. 

# Requirements

**Software**

* Python >= 3.0
* MySQL >= 5.0

**Python Modules**

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

# Script Usage

## add_feed.py

The add_feed.py script is intended to allow you to manually add new RSS Feeds to the rssbot database, via the command line. 

It is an interactive shell script that will prompt you to fill-in the blanks for the following:

* RSS Feed URL (i.e. https://somesite.com/feed.rss)
* Activate Feed (Y/N)

**Usage:**

```
./add_feed.py
```

Alternatively, you could create a web-based interface for this, either using the rssbot2.add_feed() function, inside of your web application interface code.

## runner.py

Ideally, you'd execute the runner.py script on a set interval, via crontab automation.

However, whether you execute it manually or autonomously, the command is the same.

**Usage:**

```
./runner.py
```

# Automation via cron

The main reason I wrote this script was to automate the collection of content from RSS Feeds, via cron.

## crontab interval

There are various factors to consider when determining the best interval to execute your rssbot via crontab automation.

* How many feeds am I indexing?
* How much bandwidth am I paying for on my server/vm/cloud/etc.?
* How many concurrent processes will my rssbot consume?
* How many times do I really need to 'ping' RSS Feeds?
* How much storage space is the rssbot going to consume in my database?
* How much memory will rssbot consume during it's process?

These are all valid questions. There is no single or perfect answer. It's really subjective to how/where/when you use it.

### Small RSS Feed Inventory

If you have less than 1000 feeds in your RSS feed inventory, then you should probably only run this script no more than a few times a day. 

Most likely, you'll only need to execute this script a few times a day, depending on the frequency of new content being published by the feeds that you're indexing.

### Large RSS Feed Inventory

If you have more than 1000 feeds in your RSS feed inventory, then you'll need to consider a strategy to best manage the content you're consuming. 

### Personal Blogs

Since most personal blogs publish limited amounts of content per day, you don't need to keep hammering at their feed every hour. One to two times a day is generally fine.

### Mainstream News/Blogs

Corporate/mainstream news/blog sites generally publish dozens of articles per day, so this is something to consider when determining your crontab interval. 

If the majority of your feeds are commercial content like this, you may want to index their content multiple times a day. Once an hour is generally reasonable for such a case, but keep in mind, that means 24 possoible hits per day to he same feed.

# Python Framework Integration

## Django

@todo Document this.

## Flask

@todo Document this.
