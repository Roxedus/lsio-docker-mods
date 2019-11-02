FROM lsiobase/ffmpeg:bin as binstage
FROM scratch


# Add files from binstage
COPY --from=binstage / /

# copy local files
COPY root/ /