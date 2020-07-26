# lsio-docker-mods:le-discord_f2b

Dockermod for Linuxserver.io's Letsencrypt container adding better Fail2Ban notifications for discord.

## How to use

To enable this mod, add this environment variable:
```-e DOCKER_MODS=roxedus/lsio-docker-mods:le-discord_f2b-latest```

This mod needs maxminds geolite2 database for best functionality. Get yours [here](https://dev.maxmind.com/geoip/geoip2/geolite2/)

Environment variables used by this mod:

[Discord webhook](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks), it just need the last parts. ```-e DISC_HOOK=40832456738934/7DcEpWr5V24OIEIELjg-KkHky86SrOgTqA```

[Your discord ID](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-). ```-e DISC_ME=120970603556503552```

[Map API Key](https://developer.mapquest.com/) get a key from mapquest. ```-e DISC_API=YourKey```

Arguments you can send to the action:

```bash
usage: Fail2Ban-dev.py [-h] -a {unban,ban,start,stop,test} [-d DB] [-f FAIL] [-g LOG_DIR] [-w HOOK] [-i IP] [-j JAIL] [-l {critical,error,warning,info,debug}] [-m MAP_KEY] [-u USER] [-t TIME]

Discord notifier for F2B

optional arguments:
  -h, --help            show this help message and exit
  -a {unban,ban,start,stop,test}, --action {unban,ban,start,stop,test}
                        Which F2B action triggered the script
  -d DB, --db DB        Location to geoip database
  -f FAIL, --fail FAIL  Amount of attempts done
  -g LOG_DIR, --log-dir LOG_DIR
                        Folder to store the action log.
  -w HOOK, --hook HOOK  Discord hook to use.
  -i IP, --ip IP        Ip which triggered the action
  -j JAIL, --jail JAIL  jail which triggered the action
  -l {critical,error,warning,info,debug}, --level {critical,error,warning,info,debug}
                        Sets the level of what is logged
  -m MAP_KEY, --map-key MAP_KEY
                        API key for mapquest
  -u USER, --user USER  Discord user, if it is a id, it will tag
  -t TIME, --time TIME  The time the action is valid
  ```

Arguments **override** enviroment variables. This means you can define annother Discord webhook or Discord user per action. (You can also use annoter map api key if  you really want)

| __Argument__ | __Description__ |
| --- | :--- |
|`Action` | Hopefully self-explainatory. **Required**|
|`DB` | Pass this variable with the action if your geolite database is not located as `/config/geoip2db/GeoLite2-City.mmdb`.|
|`FAIL` | This is only cosmetic, it lists the ammounts of fail-attempts invoking the ban.|
|`LOG_DIR` | You dont need this unless you are debugging.|
|`HOOK` | Pass this as an argument if you want to override the channel the webhook goes to.|
|`IP` | Used for IP lookup, and map.|
|`JAIL` | This is only cosmetic, it identifies the jail invoking the ban.|
|`LEVEL` | You dont need this unless you are debugging.|
|`MAP_KEY` | Override the map key for this action|
|`USER` | Override the mentioned user for this action.|
|`TIME` | If given a float, using `<time>` it will convert it to a timestamp. If given a int, it will say `<TIME> hours`. If given a string, you choose the time value eg. `<TIME> days`.|

Example Ban action

```ini
actionban = python3 /config/fail2ban/Fail2Ban.py -a ban -j <name> -i <ip> -t <time> -f <failures> -d /config/geoip2/GeoLite2-City.mmdb
```

## Currently tested on

linuxserver/letsencrypt

## Example

![Example picture](.assets/Example.png)1