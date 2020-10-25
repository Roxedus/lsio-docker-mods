# lsio-docker-mods:cloudflare_real-ip

Dockermod for Linuxserver.io's SWAG container adding a script to fetch the latest cloudflare ips on start

## How to use

To enable this mod, add this environment variable:
```-e DOCKER_MODS=roxedus/lsio-docker-mods:swag-cloudflare_real-ip```

To enable nginx to read the ips from this file, you need the following in your nginx.conf (or in a file included in there):

```nginx
real_ip_header X-Forwarded-For;
real_ip_recursive on;
include /config/nginx/cf_real-ip.conf;
```

You should also include your docker-network as a valid ip `set_real_ip_from 172.17.0.0/16;`
