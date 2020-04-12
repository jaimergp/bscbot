import discord
from discord.ext import commands, tasks

import requests
from datetime import datetime

import os.path

from pprint import pprint

import logging


class ChangeBanner(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.logger = logging.getLogger(__name__)

        self.change_server_banner.start()

    @tasks.loop(hours=1)
    async def change_server_banner(self):

        await self.bot.wait_until_ready()

        guild: discord.Guild = self.bot.get_guild(self.config['guild'])

        # check if guild exists
        if guild is None:
            self.bot.logger.error(
                f'Unable to change banner, guild with id {self.config["guild"]} was not found')
            return

        # check if guild is boosted (cant change banner without lvl 2 boost)
        if 'BANNER' not in guild.features:
            self.bot.logger.error(
                f'Unable to change banner, guild is not boosted')
            return

        # prepare our query
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': self.config['location'],
            'appid': self.config['api_key'],
            'units': 'metric'
        }

        # make the request
        r = requests.get(url, params)

        # check if api call succeeded
        if r.status_code != 200:
            self.bot.logger.error(
                f'Unable to change banner, weather API server returned HTTP {r.status_code}')
            return

        # load data
        json = r.json()

        # https://openweathermap.org/weather-conditions

        # todo: replace this with a nice lambda
        if json['weather'][0]['id'] > 800:  # clouds
            if self.banner_exists(801):
                await guild.edit(banner=self.banner_read(801))
                return
        if json['weather'][0]['id'] == 800:  # clear
            if self.banner_exists(800):
                await guild.edit(banner=self.banner_read(800))
                return
        if json['weather'][0]['id'] >= 700:  # atmosphere
            if self.banner_exists(700):
                await guild.edit(banner=self.banner_read(700))
                return
        if json['weather'][0]['id'] >= 600:  # snow
            if self.banner_exists(600):
                await guild.edit(banner=self.banner_read(600))
                return
        if json['weather'][0]['id'] >= 500:  # rain
            if self.banner_exists(500):
                await guild.edit(banner=self.banner_read(500))
                return
        if json['weather'][0]['id'] >= 300:  # drizzle
            if self.banner_exists(300):
                await guild.edit(banner=self.banner_read(300))
                return
        if json['weather'][0]['id'] >= 200:  # thunderstorm
            if self.banner_exists(200):
                await guild.edit(banner=self.banner_read(200))
                return

        # default case if api doesn't reply
        if self.banner_exists(0):
            await guild.edit(banner=self.banner_read(0))
            return

    def banner_exists(self, id: int) -> bool:

        path = os.path.join('assets', 'banners', f'{id}.png')
        if os.path.exists(path) is False:
            self.bot.logging.error(
                f'Unable to change banner, image with id {id} does not exist in assets/banners/ directory')
            return False

        return True

    def banner_read(self, id: int) -> bytes:

        path: str = os.path.join('assets', 'banners', f'{id}.png')
        self.bot.logger.debug(f'Loading banner from "{path}"')

        banner: bytes = open(path, mode="rb").read()
        self.bot.logger.debug(f'Read {len(banner)} bytes from file')

        if banner is None or len(banner) == 0:
            self.bot.logging.error(
                'Unable to change banner, banner is None or its size is zero')
            return

        return banner
