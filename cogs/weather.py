import discord
from discord.ext import commands
from datetime import datetime
from urllib.parse import urlencode, quote_plus
import requests


class Weather(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command(name='weather', pass_context=True)
    async def weather(self, ctx, *, location: str):

        # prepare our query
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': location,
            'appid': self.config['api_key'],
            'units': 'metric'
        }

        # make the request
        r = requests.get(url, params)

        if r.status_code != 404:
            await ctx.send(f'Location was not found 😕')
            return

        # check if api call succeeded
        if r.status_code != 200:
            await ctx.send(f'Invalid request (HTTP {r.status_code})')
            return

        # load data to dict
        json = r.json()

        # select embed color by temperature
        color = 4093670
        if json["main"]["temp"] >= 40:
            color = 15089214
        if json["main"]["temp"] >= 30:
            color = 15105086
        if json["main"]["temp"] >= 20:
            color = 15121470
        if json["main"]["temp"] >= 10:
            color = 4108006
        if json["main"]["temp"] >= 0:
            color = 4093670
        if json["main"]["temp"] <= 0:
            color = 4603622
        if json["main"]["temp"] <= -10:
            color = 4667479

        # build embed
        embed = discord.Embed(title=f'{json["name"]}, {json["sys"]["country"]}',
                              description=json["weather"][0]["description"], color=color)
        embed.add_field(name=":thermometer: Temperature",
                        value=f'{json["main"]["temp"]}°C (feels like {json["main"]["feels_like"]}°C)', inline=False)
        embed.add_field(name=":sweat_drops: Humidity",
                        value=f'{json["main"]["humidity"]}%', inline=False)
        embed.add_field(name=":dash: Wind",
                        value=f'{json["wind"]["speed"]} m/s', inline=False)
        embed.add_field(name=":cloud: Clouds",
                        value=f'{json["clouds"]["all"]}%', inline=False)

        # send embed
        await ctx.send(embed=embed)
