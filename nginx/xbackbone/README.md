# lsio-docker-mods:nginx-xbb

## You have to move this file yourself

Dockermod for Linuxserver.io's Nginx container adding xbackbone.

### How to use

To enable this mod, add this environment variable:
```-e DOCKER_MODS=roxedus/lsio-docker-mods:nginx-xbackbone-latest```

Environment variables used by this mod:

XBackbone url, the url you are serving xbackbone behind, no trailing slash. ```-e XBB_URL=http:\/\/10.0.13.160```  **Escape slashes**

XBackbone App name, the name xbackbone should use . ```-e XBB_NAME=XbackBone```

## Currently tested on

linuxserver/nginx
