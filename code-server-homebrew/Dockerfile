# syntax=docker/dockerfile:1

FROM scratch as buildstage

ADD --chmod=655 https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh /root-layer/mod-artifacts/brew.sh

COPY root/ /root-layer/

# runtime stage
FROM scratch

LABEL maintainer="Roxedus"

# Add files from buildstage
COPY --from=buildstage /root-layer/ /