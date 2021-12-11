#call module
#call module
from os import name
import discord
from discord import message, client
from discord.client import Client
from discord.ext.commands.core import check
from discord_slash import SlashCommand,SlashContext
from discord.ext import commands
import sqlite3
import asyncio
import datetime
import json
import db_cursor
import discord_token

from discord_slash.dpy_overrides import send_message

'''
ロール付与
フリチャ制作(運営への問い合わせ用)
Twitter
特定の場所に送った文章を別のチャットに飛ばす機能
サーバーを管理できる機能(BANなど)
'''

bot=commands.Bot(command_prefix='/',
                description='test',
                intents = discord.Intents.all(),
                help_command=None,
                activity=discord.Game("test") 
)

client = discord.Client()

'''
@bot.event
async def on_message(message):
    if message.author.bot:
        return None

    await bot.process_commands(message)
'''

@bot.event
async def on_ready():
    print('----------starting bot----------')

@bot.event
async def on_message(message:discord.Message):
    channel1 = 919050677362257921
    channel2 = 919050678394032178

    #ランダムなrgb値を生成するための関数
    def random_rgb():
        import random
        return random.randrange(0,255)

    #送信者がbotの場合はNoneを返す
    if message.author.bot:
        return None

    if message.channel.id == channel1:
        await message.delete() #送信されたメッセージを削除
        after_channel= bot.get_channel(channel2)#送信先のチャンネルIDを取得
        before_channel = bot.get_channel(channel1)#送信元のチャンネルIDを取得
        server_icon = message.guild.icon #送信元のサーバーアイコンを取得
        embed_forward=discord.Embed(title='メッセージ転送',colour=discord.Color.from_rgb(r=random_rgb(),g= random_rgb(),b=random_rgb()))
        embed_forward.set_author(name=message.author,icon_url=message.author.avatar)
        embed_forward.add_field(name='メッセージ内容',value=message.content,inline=False)
        embed_forward.add_field(name='送信時間',value=datetime.datetime.now())
        #サーバー画像の設定有無判定
        try:
            embed_forward.set_footer(text=message.guild.name,icon_url=server_icon)
            await after_channel.send(embed=embed_forward)
            await before_channel.send(embed=embed_forward)
        except:
            embed_forward.set_footer(text=message.guild.name)
            await after_channel.send(embed=embed_forward)
            await before_channel.send(embed=embed_forward)

    if message.channel.id == channel2:
        await message.delete() #送信されたメッセージを削除
        after_channel= bot.get_channel(channel1)#送信先のチャンネルIDを取得
        before_channel = bot.get_channel(channel2)#送信元のチャンネルIDを取得
        server_icon = message.guild.icon #送信元のサーバーアイコンを取得
        embed_forward=discord.Embed(title='メッセージ転送',colour=discord.Color.from_rgb(r=random_rgb(),g= random_rgb(),b=random_rgb()))
        embed_forward.set_author(name=message.author,icon_url=message.author.avatar)
        embed_forward.add_field(name='メッセージ内容',value=message.content,inline=False)
        embed_forward.add_field(name='送信時間',value=datetime.datetime.now())
        #サーバー画像の設定有無判定
        try:
            embed_forward.set_footer(text=message.guild.name,icon_url=server_icon)
            await after_channel.send(embed=embed_forward)
            await before_channel.send(embed=embed_forward)
        except:
            embed_forward.set_footer(text=message.guild.name)
            await after_channel.send(embed=embed_forward)
            await before_channel.send(embed=embed_forward)

    await bot.process_commands(message)


'''
@bot.slash_command(name="VoiceChannel", description="voice channel called", guild_ids=[807953798894714960])
async def channel(ctx, channel:discord.Option(discord.TextChannel, "Channel(Text)", required=True)):#, default=None, choices=["1","2","いっぱい"]
    await ctx.respond(content=channel.mention)
'''

bot.remove_command('help')
bot.run(discord_token.token())