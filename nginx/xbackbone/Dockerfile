FROM lsiobase/alpine:3.11 AS build-stage

RUN \
    apk add --no-cache curl unzip && \
    XBB_RELEASE=$(curl -sX GET "https://api.github.com/repos/SergiX44/XBackBone/releases/latest" | awk '/tag_name/{print $4;exit}' FS='[""]') && \
    echo "**** get xbb ****" && \
    mkdir -p /app/xbb/ && \
    curl -o  /tmp/xbackbone.zip -L "https://github.com/SergiX44/XBackBone/releases/download/${XBB_RELEASE}/release-v${XBB_RELEASE}.zip" && \
    unzip -q -o /tmp/xbackbone.zip -d /app/xbb/ && \
    echo "${XBB_RELEASE}" > /app/xbb/.release && \
    rm /tmp/xbackbone.zip

FROM scratch

# copy local files
COPY --from=build-stage /app/xbb/ /app/xbb/
COPY root/ /