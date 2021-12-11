#call module
from random import choice, random
import discord
from discord import message, client
from discord.client import Client
from discord.ext.commands import context
from discord.ext.commands.core import check
from discord.state import ConnectionState
from discord_slash import SlashCommand,SlashContext
from discord.ext import commands
import sqlite3
import asyncio
import datetime
import json
import db_cursor
import discord_token

from discord_slash.dpy_overrides import send_message

bot=commands.Bot(command_prefix='/',
                description='test',
                intents = discord.Intents.all(),
                help_command=None,
                activity=discord.Game("test") 
)

client = discord.Client()

#bot開始時の処理
@bot.event
async def on_ready():
    print('----------starting bot----------')

#イベントリスナー（on_message)の処理
@bot.event
async def on_message(message:discord.Message):
    channel1 = 818081875083526154
    channel2 = 919061823519617034

    #ランダムなrgb値返す関数
    def random_rgb():
        import random
        choice_random_color = ['#52bafc','#ff88ed']
        choice_random_color = random.choice(choice_random_color)
        if choice_random_color == '#52bafc':
            r=82
            g=186
            b=252 
            return r,g,b
        elif choice_random_color =='#ff88ed':
            r=255
            g=136
            b=237
            return r,g,b

    rgb_result = random_rgb()

    #送信者がbotの場合はNoneを返す
    if message.author.bot:
        return None

    if message.channel.id == channel1:
        await message.delete() #送信されたメッセージを削除
        after_channel= bot.get_channel(channel2)#送信先のチャンネルIDを取得
        before_channel = bot.get_channel(channel1)#送信元のチャンネルIDを取得
        server_icon = message.guild.icon #送信元のサーバーアイコンを取得
        embed_forward=discord.Embed(title='メッセージ転送',colour=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
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
        embed_forward=discord.Embed(title='メッセージ転送',colour=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
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

    await bot.process_commands(message) #on_message と commandsの共存させる

@bot.slash_command(name="chsetup", description="This command is a command to set the channel for message forwarding.", guild_ids=[807953798894714960])
async def ch_setup(ctx, sender:discord.Option(discord.TextChannel, "Source Channel ID", required=True), destination:discord.Option(discord.TextChannel,'Destination channel ID',required=True)):#, default=None, choices=["1","2","いっぱい"]
    #ランダムなrgb値返す関数
    def random_rgb():
        import random
        choice_random_color = ['#52bafc','#ff88ed']
        choice_random_color = random.choice(choice_random_color)
        if choice_random_color == '#52bafc':
            r=82
            g=186
            b=252 
            return r,g,b
        elif choice_random_color =='#ff88ed':
            r=255
            g=136
            b=237
            return r,g,b

    rgb_result = random_rgb()
    
    send_author_channel_id = commands.Context.channel  #送信者のチャンネルID取得
    server_icon = commands.Context.guild            #送信元のサーバーアイコンを取得
    Source_Channel_ID = sender             #送信元のIDを変数に格納
    Destination_Channel_ID = destination    #送信先のIDを変数に格納
    print(Source_Channel_ID)
    
    #セットアップの確認情報のEmbed
    channel_setup_embed = discord.Embed(title='Check setup information',description='The setup contents are as follows',colour=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
    channel_setup_embed.set_author(name=message.author,icon_url=message.author.avatar)
    channel_setup_embed.add_field(name='Source Channel ID',value=sender.content,inline=True)
    channel_setup_embed.add_field(name='Destination Channel ID',value=destination.content,inline=True)
    channel_setup_embed.add_field(name='Send time',value=datetime.datetime.now())
    #サーバー画像の設定有無判定
    try:
        channel_setup_embed.set_footer(text=message.guild.name,icon_url=server_icon)
        await send_author_channel_id.send(embed=channel_setup_embed)
    except:
        channel_setup_embed.set_footer(text=message.guild.name)
        await send_author_channel_id.send(embed=channel_setup_embed)

    db_cursor.forwarding_channel_set(before=Source_Channel_ID,after=Destination_Channel_ID) #データベースに登録
    

bot.remove_command('help')
bot.run(discord_token.token())