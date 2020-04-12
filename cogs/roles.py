import discord
from discord.ext import commands, tasks
from datetime import datetime


class Roles(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.role_cache = []

    @commands.command(name='role', pass_context=True)
    async def assign(self, ctx, *, requested_role=None):

        # allow this command only in control channel
        if ctx.channel.id != self.config['channel']:
            return

        # build role cache if it is empty
        if len(self.role_cache) == 0:
            for role in ctx.guild.roles:
                if [item for item in self.config['roles'] if item == role.id]:
                    self.role_cache.append(role)

        # send available roles if argument is not supplied
        if requested_role is None:
            roles = ', '.join([item.name for item in sorted(self.role_cache)])
            await ctx.send(f'Available roles: {roles}')
            return

        # remove all existing listed roles
        for role in ctx.message.author.roles:
            if [item for item in self.config['roles'] if item == role.id]:
                await ctx.message.author.remove_roles(role)

        # find applicable role and add it to the user
        for role in ctx.guild.roles:
            if [item for item in self.config['roles'] if item == role.id] and role.name.lower() == requested_role.lower():
                # add role and reply to the user
                await ctx.message.author.add_roles(role)
                await ctx.send(f'{ctx.message.author.mention}: Added role "{role.name}"')
                return

        await ctx.send(f'{ctx.message.author.mention}: Role was not found.')
        return