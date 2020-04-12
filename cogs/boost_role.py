import discord
from discord.ext import commands, tasks

import requests
from datetime import datetime

from pprint import pprint


class BoostRole(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

        self.check_users_for_role.start()

    @tasks.loop(minutes=10)
    async def check_users_for_role(self):

        await self.bot.wait_until_ready()

        guild: discord.Guild = self.bot.get_guild(self.config['guild'])

        # check if guild exists
        if guild is None:
            self.bot.logger.error(
                f'Unable check for boosters, guild with id {self.config["guild"]} was not found')
            return

        boost_role: discord.Role = guild.get_role(self.config['boost_role'])

        # check if role exists
        if boost_role is None:
            self.bot.logger.error(
                f'Unable check for boosters, role with id {self.config["boost_role"]} was not found')
            return

        # iterate all server members
        user: discord.Member
        for user in guild.members:

            # get booleans for role/boost comparison
            has_boosted_role: bool = len(
                [role for role in user.roles if role == boost_role]) > 0
            has_boosted_guild: bool = isinstance(user.premium_since, datetime)

            if has_boosted_guild and has_boosted_role == False:
                self.bot.logger.info(
                    f'Adding booster role "{boost_role.name}"" for user "{user.nick}"')

                await user.add_roles(boost_role)
                return

            if has_boosted_guild == False and has_boosted_role:
                self.bot.logger.info(
                    f'Removing booster role "{boost_role.name}"" from user "{user.nick}"')
                await user.remove_roles(boost_role)
                return
