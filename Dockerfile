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

	# # install rssbot2 release
	# && wget "https://github.com/sodonnell/rssbot2/archive/v${RSSBOT_VERSION}.tar.gz" -O /tmp/rssbot.v${RSSBOT_VERSION}.tar.xz \
	# && mkdir -p $HOME/rssbot2 \
	# && tar -xf /tmp/rssbot.v${RSSBOT_VERSION}.tar.xz -C $HOME/rssbot2 \
	# && rm /tmp/rssbot.v${RSSBOT_VERSION}.tar.xz \
	# && cd $HOME/rssbot2 \
	#&& rm -rf /var/lib/apt/lists/* \

    # # setup rssbot
	# && pip3 install -r requirements.txt \
	# && ./setup.py \
	# 	-u rssbot2 \
	# 	-p rssbot2 \
	# 	-h localhost \
	# 	-d rssbot2

# configure system user account
RUN useradd -rm -d $HOME -s /bin/bash -g root -G sudo -u 1000 rssbot -p "$(openssl passwd -1 rssbot)"
USER rssbot
WORKDIR $HOME

CMD ["bash"]
