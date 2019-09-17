# rssbot2

A modern version of my ancient rssbot module, written in python3.

| Branch | Build Status |
|-|-|
| master | [![Build Status](https://travis-ci.org/sodonnell/rssbot2.svg?branch=master)](https://travis-ci.org/sodonnell/rssbot2) |
| development | [![Build Status](https://travis-ci.org/sodonnell/rssbot2.svg?branch=development)](https://travis-ci.org/sodonnell/rssbot2) |

![Github issues](https://img.shields.io/github/issues/sodonnell/rssbot2)
![Github forks](https://img.shields.io/github/forks/sodonnell/rssbot2)
![Github stars](https://img.shields.io/github/stars/sodonnell/rssbot2)
![Github license](https://img.shields.io/github/license/sodonnell/rssbot2)

<!-- TOC -->
- [Overview](#overview)
  - [Requirements](#requirements)
    - [Hardware](#hardware)
    - [Software](#software)
    - [PiPy Modules](#pipy-modules)
  - [Installation](#installation)
- [Script Usage](#script-usage)
  - [add_feed.py](#addfeedpy)
  - [runner.py](#runnerpy)
- [Wiki Documentation](#wiki-documentation)
<!-- /TOC -->

## Overview

The rssbot2 python script is intended to monitor a random list of RSS Feeds that are defined within a mysql database table, on a continuous basis, and gather/add any new articles (links) that have been published since the last monitoring session.

### Requirements

#### Hardware

#### Software

- Python >= 3.6
- MySQL >= 5.0

#### PiPy Modules

- configobj
- feedparser
- mysql-connector-python

### Installation

It's pretty straight-forward.

1) Clone this repo.
2) Install the dependencies.
3) Run the setup.py script.
4) Enter the database configuration information during the setup process.

```bash
git clone https://github.com/sodonnell/rssbot2.git
cd rssbot2
pip3 install -r requirements.txt
python3 setup.py
```

The setup.py script will create a new database schema, if the one you specify doesn't already exist. All you should need is a valid username, password and hostname for your database server.

Alternatively, you can pass arguments when you call the setup.py script. Use the --help argument to see the available arguments.

```bash
python3 setup.py --help
```

**Example:**

```bash
python3 setup.py -u rssbot -d rssbot -h localhost
```

Any of the arguments that you prefer not to include, will prompt you for user input. Specifically, we do not suggest using the -p or --password arguments. These are mainly for automated testing in travisci, but you're on your own if you do.

## Script Usage

### add_feed.py

The add_feed.py script is intended to allow you to manually add new RSS Feeds to the rssbot database, via the command line.

It is an interactive shell script that will prompt you to fill-in the blanks for the following:

- RSS Feed URL (i.e. https://somesite.com/feed.rss)
- Activate Feed (Y/N)

**Usage:**

```
python3 add_feed.py
```

The add_feed.py script also supports the arguments:

```
python3 add_feed.py -u https://somesite.com/feed.rss -a
```

Alternatively, you could create a web-based interface, instead, but that's outside the scope of this project.

### runner.py

Ideally, you'd execute the runner.py script on a set interval, via crontab automation. However, whether you execute it manually or autonomously, the command is the same.

**Usage:**

```
python3 runner.py
```

Feel free to extend the runner.py script as you see fit, for your application-specific requirements.

## Wiki Documentation

- [Automating runner.py via cron](https://github.com/sodonnell/rssbot2/wiki/Automating-runner.py-via-cron)
- [Python Framework Integration](https://github.com/sodonnell/rssbot2/wiki/Python-Framework-Integration)