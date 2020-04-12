import discord
from discord.ext import commands, tasks
from datetime import datetime

from pprint import pprint


class Monitor(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    # on message delete
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        channel = self.bot.get_channel(self.config['channel'])

        embed = discord.Embed(title=f"Message deleted in #{message.channel.name}",
                              description=f"{message.author.name}#{message.author.discriminator}", color=0xff7578)
        embed.add_field(
            name="Content", value=f"{message.content}", inline=True)
        embed.add_field(name="Id", value=f"{message.id}", inline=False)
        embed.add_field(name="Message Date",
                        value=f"{message.created_at}", inline=True)

        await channel.send(embed=embed)

    # on message edit
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        channel = self.bot.get_channel(self.config['channel'])

        embed = discord.Embed(title=f"Message edited in #{before.channel.name}",
                              description=f"{before.author.name}#{before.author.discriminator}", color=0xff7578)
        embed.add_field(name="Content Before",
                        value=f"{before.content}", inline=False)
        embed.add_field(name="Content After",
                        value=f"{after.content}", inline=False)
        embed.add_field(name="Id", value=f"{before.id}", inline=False)
        embed.add_field(name="Message Date",
                        value=f"{before.created_at}", inline=True)

        await channel.send(embed=embed)

    # on member join
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(self.config['channel'])

        embed = discord.Embed(title="User joined server",
                              description=member.name, color=0x9ad658)
        embed.add_field(name="Id", value=member.id, inline=False)
        embed.add_field(name="Joined At", value=member.joined_at, inline=True)

        await channel.send(embed=embed)

    # on member remove
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = self.bot.get_channel(self.config['channel'])

        embed = discord.Embed(title="User left server",
                              description=member.name, color=0x9ad658)
        embed.add_field(name="Id", value=member.id, inline=False)
        embed.add_field(name="Joined At", value=member.joined_at, inline=True)

        await channel.send(embed=embed)

    # on user update (avatar, username, discriminator)
    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        channel = self.bot.get_channel(self.config['channel'])

        if before.avatar != after.avatar:
            embed = discord.Embed(title="User updated", color=0x8666c8)
            embed.add_field(name="", value="", inline=False)
            embed.add_field(name="Avatar Before",
                            value=before.avatar_url, inline=False)
            embed.add_field(name="Avatar After",
                            value=after.avatar_url, inline=False)
            embed.add_field(name="Id", value=before.id, inline=True)

            await channel.send(embed=embed)

        if before.username != after.avatar:
            embed = discord.Embed(title="User updated", color=0x8666c8)
            embed.add_field(name="", value="", inline=False)
            embed.add_field(name="Username Before",
                            value=before.display_name, inline=False)
            embed.add_field(name="username After",
                            value=after.display_name, inline=False)
            embed.add_field(name="Id", value=before.id, inline=True)

            await channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = discord.Embed(title="User updated", color=0x8666c8)
            embed.add_field(name="", value="", inline=False)
            embed.add_field(name="Discriminator Before",
                            value=before.discriminator, inline=False)
            embed.add_field(name="Discriminator After",
                            value=after.discriminator, inline=False)
            embed.add_field(name="Id", value=before.id, inline=True)

            await channel.send(embed=embed)
