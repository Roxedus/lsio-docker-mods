#!/usr/bin/env python3
import argparse
import collections
import ipaddress
import logging
import logging.handlers
import os
import sys
from datetime import datetime

import pytz
import requests

import geoip2.database

has_geo = True


class Logger(object):
    def __init__(self, folder, level):
        self.folder = folder
        self.log_level = level.upper()

        self.logger = logging.getLogger("DiscordEmbed")
        self.logger.setLevel(self.log_level)

        log_formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(module)s : %(message)s', '%Y-%m-%d %H:%M:%S')

        if folder:
            self.log_dir = self.folder + '/DiscordEmbed.log'

            if not os.path.isdir(self.folder):
                os.makedirs(self.folder)
                self.logger.debug("Creating logging directory: %s" % self.folder)
            self.logger.debug("Logging directory: %s" % self.log_dir)
            file_handler = logging.handlers.RotatingFileHandler(self.log_dir, mode='a',
                                                                maxBytes=5000, encoding="UTF-8", delay=0, backupCount=5)
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(log_formatter)
            self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(self.log_level)

        self.logger.addHandler(console_handler)


class Discord(object):
    def __init__(self, **kwargs):
        self.discord_url = "https://discordapp.com/api/webhooks/"
        self.hook_user = "Fail2Ban"
        self.action = kwargs.get("action")
        self.fails = kwargs.get("fails")
        self.hook = kwargs.get("hook")
        self.ip = kwargs.get("ip")
        self.jail = kwargs.get("jail")
        self.time = kwargs.get("time")
        self.user = kwargs.get("user")
        if has_geo:
            self.geodata = helper.geodata()
            try:
                self.map_url, self.map_img = helper.map(self.geodata["lon"], self.geodata["lat"])
            except ValueError:
                self.map_url = helper.map(self.geodata["lon"], self.geodata["lat"])

    def create_payload(self):
        webhook = {
            "username": self.hook_user,
            "content": f"<@{self.user}>",
            "embeds": [
                {
                    "author": {"name": self.hook_user},
                    "timestamp": f"{datetime.utcnow()}"
                }
            ]
        }
        if "ban" in self.action:
            if has_geo:
                embed = {
                    "url": f"https://db-ip.com/{self.ip}",
                    "fields": [
                        {
                            "name": f":flag_{self.geodata['iso'].lower()}:",
                            "value": self.geodata["city"] or self.geodata["name"]
                        }
                    ]
                }
            if self.map_img:
                embed["image"] = {"url": f"{self.map_img}"}
            if self.action == "ban":
                embed["fields"].append({"name": "Map", "value": f"[Link]({self.map_url})"})
                embed["fields"].append({"name": "Unban cmd", "value": f"```bash\nfail2ban-client unban {self.ip}```"})
                ban_embed = {
                    "title": f"New ban on `{self.jail}`",
                    "color": 16194076
                }
                try:
                    embed["description"] = f"**{self.ip}** got banned for `{int(self.time)}` hours after `{self.fails}` tries"
                except ValueError:
                    time = datetime.fromtimestamp(float(self.time),
                                                  tz=pytz.timezone(os.getenv('TZ'))
                                                  ).strftime('%Y-%m-%d %H:%M:%S %Z%z')
                    embed["description"] = f"**{self.ip}** got banned for `{self.fails}` failed attempts, unbanning at `{time}`"
                except ValueError:
                    embed["description"] = f"**{self.ip}** got banned for `{self.time}` after `{self.fails}` tries"
                embed.update(ban_embed)
            elif self.action == "unban":
                unban_embed = {
                    "title": f"Revoked ban on `{self.jail}`",
                    "description": f"**{self.ip}** is now unbanned",
                    "color": 845872
                }
                embed.update(unban_embed)
            webhook["embeds"][0].update(embed)
        elif self.action == "start":
            webhook["content"] = ""
            webhook["embeds"][0]["description"] = f"Started `{self.jail}`"
            webhook["embeds"][0]["color"] = 845872
        elif self.action == "stopped":
            webhook["content"] = ""
            webhook["embeds"][0]["description"] = f"Stopped `{self.jail}`"
            webhook["embeds"][0]["color"] = 16194076
        elif self.action == "test":
            webhook["content"] = ""
            webhook["embeds"][0]["description"] = f"I am working"
            webhook["embeds"][0]["color"] = 845872
        else:
            return None
        logger.debug('Webhook: %s' % webhook)
        return webhook

    def send(self, payload):
        logger.debug('Payload: %s' % payload)
        r = requests.post(url=f"{self.discord_url}{self.hook}", json=payload)
        logger.info('Sent webhook, Status: %s' % r.status_code)


class Helpers(object):
    def __init__(self, **kwargs):
        self.geoipDB = kwargs.get('geoipDB')
        self.map_key = kwargs.get('map_key')
        self.ip = kwargs.get('ip')
        self.private = ipaddress.ip_address(self.ip).is_private

        if self.private:
            has_geo = False
            logger.warning('%s is a local ip, continuing without geodata' % self.ip)

        try:
            self.reader = geoip2.database.Reader(self.geoipDB)
        except FileNotFoundError:
            has_geo = False
            logger.warning('GeoIP database not found in %s, continuing without geodata' % self.geoipDB)
        except Exception as e:
            logger.error('FATAL ERROR: %s' % e)

    def geodata(self):
        r = self.reader.city(self.ip)
        return {'iso': r.country.iso_code, "name": r.country.name,
                "city": r.city.name, "lat": r.location.latitude,
                "lon": r.location.longitude}

    def map(self, lon, lat):
        s = requests.Session()

        url_params = {"center": f"{lat},{lon}", "size": "500,300"}
        url_r = s.get('https://mapquest.com/', params=url_params).url

        try:
            img_params = {"center": f"{lat},{lon}", "size": "500,300", "key": self.map_key}
            img_r = s.get('https://www.mapquestapi.com/staticmap/v5/map', params=img_params)
            assert img_r.status_code == 200
            return url_r, img_r.url
        except AssertionError:
            logger.warning('Map api not found')
            return url_r


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Discord notifier for F2B')
    parser.add_argument('-a', '--action', help="Which F2B action triggered the script", required=True)
    parser.add_argument('-d', '--db', help="Location to geoip database", default='/config/geoip2db/GeoLite2-City.mmdb')
    parser.add_argument('-f', '--fail', help="Amount of attempts done")
    parser.add_argument('-g', '--log-dir', help="Folder to store the action log.")
    parser.add_argument('-w', '--hook', help="Discord hook to use.")
    parser.add_argument('-i', '--ip', help="Ip which triggered the action", default="1.1.1.1")
    parser.add_argument('-j', '--jail', help="jail which triggered the action")
    parser.add_argument('-l', '--level', help="Sets the level of what is logged", default="info",
                        choices=["critical", "error", "warning", "info", "debug"])
    parser.add_argument('-m', '--map-key', help="API key for mapquest")
    parser.add_argument('-u', '--user', help="Discord user, if it is a id, it will tag")
    parser.add_argument('-t', '--time', help="The time the action is valid")

    args = parser.parse_args()

    if not args.map_key:
        args.map_key = os.getenv('DISC_API')
    if not args.hook:
        args.hook = os.getenv('DISC_HOOK')
    if not args.user:
        args.user = os.getenv('DISC_ME')

    logger = Logger(folder=args.log_dir, level=args.level).logger
    helper = Helpers(geoipDB=args.db, map_key=args.map_key, ip=args.ip)
    disc = Discord(action=args.action, fails=args.fail, hook=args.hook,
                   ip=args.ip, jail=args.jail, time=args.time, user=args.user)

    if (payload:= disc.create_payload()):
        disc.send(payload)
