# Homebrew - Docker mod for code-server/openvscode-server

This mod adds `Homebrew` to code-server/openvscode-server, to be installed/updated during container start.

In code-server/openvscode-server docker arguments, set an environment variable `DOCKER_MODS=ghcr.io/roxedus/lsio-docker-mods:code-server-homebrew-latest`

`Homebrew` is installed at to the default prefix at `/home/linuxbrew/.linuxbrew`. It is recommended to mount `/home/linuxbrew` for persistence.

This mod does not prepare the shell to use brew, you have to edit your rc file yourself for this. You can do this by adding `eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"` to your rc file.

Brew can also aid with shell completions, you have to manually enable this too, visit the [docs](https://docs.brew.sh/Shell-Completion) for how to do this.
