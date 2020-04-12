from discord.ext import commands
from discord import ActivityType
from cogs.roles import Roles
from cogs.youtube import Youtube
from cogs.weather import Weather
from cogs.role_distribution import RoleDistribution
from cogs.monitor import Monitor
from cogs.change_banner import ChangeBanner
from cogs.boost_role import BoostRole
import random
import logging
import json


def run_bot():
    # load config from json file
    config = json.load(open('config.json'))

    # initialize bot instance
    bot = commands.Bot(command_prefix='!')
    bot.logger = logging.getLogger('discord')

    # add cogs and load their individual configs
    bot.add_cog(
        Monitor(bot, [item for item in config['cogs'] if item['name'] == 'monitor'][0]))
    bot.add_cog(
        ChangeBanner(bot, [item for item in config['cogs'] if item['name'] == 'banner'][0]))
    # bot.add_cog(
    #     Weather(bot, [item for item in config['cogs'] if item['name'] == 'weather'][0]))
    bot.add_cog(
        Roles(bot, [item for item in config['cogs'] if item['name'] == 'roles'][0]))
    bot.add_cog(
        BoostRole(bot, [item for item in config['cogs'] if item['name'] == 'boost'][0]))

    # set random presence on start
    '''
    @bot.event
    async def on_ready():
        actions = {
            0: lambda: bot.change_presence(activity=Activity(name='something', type=ActivityType.playing)),
            1: lambda: bot.change_presence(activity=Activity(name='something', type=ActivityType.listening)),
            2: lambda: bot.change_presence(activity=Activity(name='something', type=ActivityType.watching))
        }

        await actions[random.randint(0, len(actions) - 1)]()
    '''

    bot.run(config['bot']['token'])


if __name__ == '__main__':
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(
        filename='logs/discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    run_bot()
