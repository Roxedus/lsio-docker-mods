# lsio-docker-mods:le-discord_f2b

Dockermod for Linuxserver.io's Letsencrypt container adding better Fail2Ban notifications for discord.

#### How to use:
[In-depth guide](https://github.com/linuxserver/docker-mods#using-a-docker-mod) 

Add this environment variable: 
```-e DOCKER_MODS=roxedus/lsio-docker-mods:le-discord_f2b-latest```

Environment variables used by this mod:
```-e DISC_HOOK=40832456738934/7DcEpWr5V24OIEIELjg-KkHky86SrOgTqA```


```-e DISC_ME="120970603556503552```

Add this action to your jail: `discordEmbed[bantime=24]`

## Currently tested on:  
linuxserver/letsencrypt
