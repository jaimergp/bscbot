import discord
from discord.ext import commands, tasks
from datetime import datetime


class RoleDistribution(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command(name='distribution', pass_context=True)
    async def role_distribution(self, ctx):
        pass
