import json
import asyncio
from discord.ext import commands
from cogs.command_peak import get_embed

config = json.load(open('config.json'))

client = commands.Bot(command_prefix=config['prefix'])


@client.event
async def on_ready():
    while True:
        ids = json.load(open('config.json'))
        while ids['message_id'] == -1:
            ids = json.load(open('config.json'))
            print("Please set a channel with the 'peak' command.")
            await asyncio.sleep(5)
        try:
            msg = await \
                client.get_guild(ids['server_id']).get_channel(ids['channel_id']).fetch_message(ids['message_id'])
            await msg.edit(embed=get_embed())
        except:
            pass
        await asyncio.sleep(60)


@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx):
    client.unload_extension('cogs.command_peak')
    client.load_extension('cogs.command_peak')
    await ctx.send("Reloaded.")
    print("Reloaded peak cog.")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass

client.load_extension('cogs.command_peak')
client.run(config['token'])
