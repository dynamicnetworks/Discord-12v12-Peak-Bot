import json
import discord
import datetime
import requests
from discord.ext import commands


def get_embed():
    info = Info()
    board = info.get_peaks()
    now = datetime.datetime.now()
    current_time = str(now.strftime("%I:%M:%S"))
    board.sort(reverse=True)
    timestamp_list = []
    peak_list = []

    for peak in board:
        date = datetime.datetime.fromtimestamp(peak[0] / 1e3)
        timestamp_list.append(date.strftime("%b %d"))
        peak_list.append(peak[1])

    embed = discord.Embed(
        color=0x7E1212,
        title="Current Peaks For Last 30 Days",
    )
    embed.add_field(name="Date", value="{}".format('\n'.join(timestamp_list)), inline=True)
    embed.add_field(name="Peak", value="{}".format('\n'.join(str(peak) for peak in peak_list)), inline=True)
    embed.set_footer(text="Last updated at: " + current_time + " CST")
    embed.set_thumbnail(
        url="https://steamuserimages-a.akamaihd.net/ugc/1244631126935143961/5A8B4A6E5E7995FA06E1D18025DBCB2DED15D3D3/")
    return embed


class Info:
    def __init__(self):
        self.url = "https://api.dotaworkshop.com/v1/GetDailyPeaks/1576297063"

    def get_list(self):
        return requests.request("GET", self.url).text

    def get_peaks(self):
        peaks = json.loads(self.get_list())[-30:]
        board = []
        for peak in peaks:
            board.append([
                peak["timestamp"],
                peak["dailyPeak"]
            ])
        return board


class Peak(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def peak(self, ctx):
        message = await ctx.send(embed=get_embed())

        message_id = message.id
        channel_id = message.channel.id
        guild_id = message.guild.id

        with open('config.json') as f:
            config = json.load(f)
        config['message_id'] = message_id
        config['channel_id'] = channel_id
        config['server_id'] = guild_id

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)


def setup(client):
    client.add_cog(Peak(client))
