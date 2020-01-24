FROM debian:latest

ENV HOME /home/rssbot
ENV HOSTNAME rssbot.local
ENV LANG en_US.utf8
ENV RSSBOT_VERSION 2.0.0

# install base package and dependencies
RUN apt-get update && rm -rf /var/lib/apt/lists/*

RUN packages=' \
		autoconf \
		automake \
		bzip2 \
		ca-certificates \
		dirmngr \
		dpkg-dev \
		git \
		gnupg \
		htop \
		less \
		libglib2.0-0 \
		libglib2.0-dev \
		libncurses-dev \
		libssl-dev \
		libtool \
		lynx \
		make \
		net-tools \
		pkg-config \
		sudo \
        mariadb-server \
        python3 \
        python3-pip \
		wget \
		vim \
		xz-utils \
	' \
	&& set -x \
	&& apt-get update && apt-get install -y $packages --no-install-recommends

RUN ln -s /usr/bin/python3 /usr/bin/python

# configure mysql db+user
RUN /etc/init.d/mysql start \
    && mysql -u root -e "create database rssbot2;" \
    && mysql -u root -e "create user rssbot2 identified by 'rssbot2'; grant all on rssbot2.* to rssbot2;"

# configure system user account
RUN useradd -rm -d $HOME -s /bin/bash -g root -G sudo -u 1000 rssbot -p "$(openssl passwd -1 rssbot)"
USER rssbot
WORKDIR $HOME

# setup rssbot2
RUN git clone https://github.com/sodonnell/rssbot2.git \
&& cd rssbot2 \
&& git checkout docker \
&& pip3 install -r requirements.txt \
&& python3 setup.py -h localhost -u rssbot2 -d rssbot2 -p rssbot2 \
&& python3 add_feed.py -a -u https://phys.org/rss-feed/ \
&& python3 add_feed.py -a -u https://hackaday.com/blog/feed/ \
&& python3 add_feed.py -a -u https://www.wired.com/feed/rss \
&& python3 runnser.py \
&& crontab crontab

CMD ["bash"]
