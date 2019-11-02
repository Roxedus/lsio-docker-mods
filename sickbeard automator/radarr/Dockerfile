FROM lsiobase/ffmpeg:bin as binstage

# Add files from binstage
COPY --from=binstage / /

# copy local files
COPY root/ /