# lsio-docker-mods:le-discord_f2b

Dockermod for Linuxserver.io's Letsencrypt container adding better Fail2Ban notifications for discord.

#### How to use:
[In-depth guide](https://github.com/linuxserver/docker-mods#using-a-docker-mod) 

Add this environment variable:  
```-e DOCKER_MODS=roxedus/lsio-docker-mods:le-discord_f2b-latest```



Environment variables used by this mod:  
[Discord webhook](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks), it just need the last parts. ```-e DISC_HOOK=40832456738934/7DcEpWr5V24OIEIELjg-KkHky86SrOgTqA```  
[Your discord ID](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-). ```-e DISC_ME=120970603556503552```

Add this action to your jail: `discordEmbed[bantime=24]`, `bantime`(hour) is optional, but defaults to 24 when not set. Just reflects in the message, does not change the ban time

## Currently tested on:  
linuxserver/letsencrypt
