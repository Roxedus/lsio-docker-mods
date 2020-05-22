FROM scratch

RUN \
    mkdir -p /app/xbb/ && \
    XBB_RELEASE=$(curl -sX GET "https://api.github.com/repos/SergiX44/XBackBone/releases/latest" | awk '/tag_name/{print $4;exit}' FS='[""]'); && \
    echo "**** get xbb ****" && \
    curl -o  /tmp/xbackbone.zip -L "https://github.com/SergiX44/XBackBone/releases/download/${XBB_RELEASE}/release-v${XBB_RELEASE}.zip" && \
    unzip -q -o /tmp/xbackbone.zip -d /app/xbb/ && \
    echo "${XBB_RELEASE}" > /app/xbb/.release && \
    rm /tmp/xbackbone.zip


# copy local files
COPY root/ /