import discord
from discord.ext import commands, tasks

import requests
from datetime import datetime

from pprint import pprint


class Youtube(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.time = f'{datetime.utcnow().isoformat()}Z'

        self.check_videos.start()

    @tasks.loop(minutes=1)
    async def check_videos(self):

        await self.bot.wait_until_ready()

        for channel in self.config['channels']:

            url = 'https://www.googleapis.com/youtube/v3/search'
            query = {
                'part': 'snippet',
                'channelId': channel,
                'maxResults': 10,
                'order': 'date',
                'type': 'video',
                'key': self.config['api_key']
            }

            r = requests.get(url, query)

            json = r.json()

            for video in json['items']:
                channel = self.bot.get_channel(self.config['channel'])

                if video['snippet']['publishedAt'] <= self.time:
                    continue

                video_url = f'https://www.youtube.com/watch?v={video["id"]["videoId"]}'
                channel_url = f'https://www.youtube.com/channel/{video["snippet"]["channelId"]}'

                embed = discord.Embed()
                embed.title = f'{video["snippet"]["title"]}'
                embed.description = video["snippet"]["description"]
                embed.color = 0x3498db
                embed.url = video_url
                embed.set_author(
                    name=video["snippet"]["channelTitle"], url=channel_url)
                embed.set_thumbnail(
                    url=video['snippet']['thumbnails']['default']['url'])
                embed.set_footer(text=video['snippet']['publishedAt'])

                await channel.send(embed=embed)

        self.time = f'{datetime.now().isoformat()}Z'
