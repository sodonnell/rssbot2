FROM debian:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
		ca-certificates \
		libglib2.0-0 \
        mysql-server \
		wget \
        python3 \
        python3-pip \
	&& rm -rf /var/lib/apt/lists/*

ENV HOME /home/rssbot
RUN useradd --create-home --home-dir $HOME rssbot \
	&& mkdir -p $HOME/.rssbot \
	&& chown -R rssbot:rssbot $HOME

ENV LANG en_US.utf8

ENV RSSBOT_VERSION 2.0.2

RUN buildDeps=' \
		autoconf \
		automake \
		bzip2 \
		dirmngr \
		dpkg-dev \
		gnupg \
		libglib2.0-dev \
		libncurses-dev \
		libssl-dev \
		libtool \
		lynx \
		make \
		pkg-config \
		xz-utils \
	' \
	&& set -x \
	&& apt-get update && apt-get install -y $buildDeps --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/* \
	&& wget "https://github.com/sodonnell/rssbot2/archive/v2.0.0.tar.gz" -O /tmp/rssbot.v2.0.0.tar.xz \
	&& mkdir -p $HOME/rssbot2 \
	&& tar -xf /tmp/rssbot.v2.0.0.tar.xz -C $HOME/rssbot2 \
	&& rm /tmp/rssbot.v2.0.0.tar.xz \
	&& cd $HOME/rssbot2 \
    # configure mysql
    && mysql -u root -e "create database rssbot2;" \
    && mysql -u root -e "create user rssbot2 identified by 'rssbot2'; grant all on rssbot2.* to rssbot2;" \
    # setup rssbot
	&& pip3 install -r requirements.txt \
	&& ./setup.py \
		-u rssbot2 \
		-p rssbot2 \
		-h localhost \
		-d rssbot2

WORKDIR $HOME

USER rssbot
CMD ["bash"]