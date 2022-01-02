#call module
from os import name
from random import choice, random
import discord
from discord import message, client
from discord import guild
from discord.client import Client
from discord.ext.commands import context
from discord.ext.commands.core import check, command
from discord.state import ConnectionState
from discord_slash import SlashCommand,SlashContext
from discord.ext import commands
import sqlite3
import asyncio
import datetime
import json
import discord_token
import os
from discord_slash.dpy_overrides import send_message
import id_db
import string
import time

bot=commands.Bot(command_prefix='/',
                description='test',
                intents = discord.Intents.all(),
                help_command=None,
                activity=discord.Game("test") 
)
client = discord.Client()

def random_rgb() -> tuple:
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
#ランダムなrgb値返す関数
rgb_result = random_rgb()
now = datetime.datetime.now()
os.chdir(os.getcwd())

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
        embed_forward = discord.Embed(title='～メッセージ転送～',colour=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
        embed_forward.set_author(name=message.author.display_name,icon_url=message.author.avatar)
        embed_forward.add_field(name='メッセージ内容',value=message.content,inline=False)
        embed_forward.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}")
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

        after_channel = bot.get_channel(channel1)#送信先のチャンネルIDを取得
        before_channel = bot.get_channel(channel2)#送信元のチャンネルIDを取得
        server_icon = message.guild.icon #送信元のサーバーアイコンを取得

        embed_forward=discord.Embed(title='～メッセージ転送～',colour=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
        embed_forward.set_author(name=message.author.display_name,icon_url=message.author.avatar)
        embed_forward.add_field(name='メッセージ内容',value=message.content,inline=False)
        embed_forward.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}")

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

@bot.slash_command(name="chsetup", description="このコマンドはメッセージを転送するチャンネルを設定するものです。", guild_ids=[807953798894714960])
async def ch_setup(ctx, channel1:discord.Option(discord.TextChannel, "チャンネルを選択してください", required=True), channel2:discord.Option(discord.TextChannel,'チャンネルを選択してください',required=True)):#, default=None, choices=["1","2","いっぱい"]
    send_author_channel_id = ctx.channel.id  #送信者のチャンネルID取得
    send_author_channel_id = bot.get_channel(send_author_channel_id)
    Channel1_ID = channel1.id               #送信元のIDを変数に格納
    Channel2_ID = channel2.id               #送信先のIDを変数に格納
    Channel1_name = channel1.name
    Channel2_name = channel2.name
    id_db.forwarding_channel_set(channel1=Channel1_ID,channel2=Channel2_ID)

    #セットアップの確認情報のEmbed
    channel_setup_embed = discord.Embed(title='メッセージ転送（設定）',description='メッセージを転送するチャンネルを以下のように設定しました。',colour=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
    channel_setup_embed.add_field(name='Channel1 ID',value=Channel1_ID,inline=True)
    channel_setup_embed.add_field(name='Channel2 ID',value=Channel2_ID,inline=False)
    channel_setup_embed.add_field(name='Channel1 name',value=Channel1_name,inline=True)
    channel_setup_embed.add_field(name='Channel2 name',value=Channel2_name,inline=False)
    channel_setup_embed.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=False)
    await ctx.respond(embed=channel_setup_embed)

@bot.slash_command(name='inquiry_setting',description='このコマンドはお問い合わせ先のユーザーを誰にするか決めることができます。（※管理者権限がないと実行できません）',guild_ids=[807953798894714960])
@commands.has_permissions(administrator = True)
async def slash_command_inquirysetting(ctx,who:discord.Option(discord.Member,'お問い合わせ先のユーザーを選択してください',Required=True)):
    user_id = who.id            #userID取得
    guild_id = ctx.guild.id    #guildID取得
    entry_check=id_db.inquiry_set(guild=guild_id,user=user_id)
    #dbに登録
    if entry_check == False:
        inquiry_bad_embed=discord.Embed(title='～お問い合わせ（設定エラー）～',description='お問い合わせ先のユーザーが重複して設定しようとしている可能性があります。（お問い合わせ先ユーザーは２人以上は設定することはできません。）登録者名を変更するために「/inquiry_update」を実行してください。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
        await ctx.respond(embed=inquiry_bad_embed)
    else:
        #確認のembedを送信
        inquiry_setting_embed=discord.Embed(title='～お問い合わせ（設定）～',description='お問い合わせ先のユーザーを以下のユーザーに設定します。',color=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
        inquiry_setting_embed.add_field(name='ユーザー名',value=who.mention,inline=True)
        inquiry_setting_embed.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=True)
        inquiry_setting_embed.add_field(name='ユーザーID',value=who.id,inline=False)
        inquiry_setting_embed.add_field(name='サーバーID（ギルドID）',value=guild_id,inline=True)
        inquiry_setting_embed.set_thumbnail(url=who.avatar)
        #サーバー画像の設定有無判定
        try:
            server_icon = ctx.guild.icon
            inquiry_setting_embed.set_footer(text=ctx.guild.name,icon_url=server_icon)
            await ctx.respond(embed=inquiry_setting_embed)
        except:
            inquiry_setting_embed.set_footer(text=ctx.guild.name)
            await ctx.respond(embed=inquiry_setting_embed)

@bot.slash_command(name='inquiry_update',description='このコマンドではお問い合わせユーザーの変更を変更します。（※管理者権限がないと実行できません）',guild_ids=[807953798894714960])
@commands.has_permissions(administrator = True)
async def slash_command_inquiryupdate(ctx,who:discord.Option(discord.Member,'ユーザーを選択してください。',required=True)):
    guild_id = ctx.guild.id
    user_id = who.id
    entry_check = id_db.inquiry_update(guild=guild_id,user=user_id)
    if entry_check == False:
        inquiry_bad_embed=discord.Embed(title='～お問い合わせ（設定エラー）～',description='お問い合わせユーザーが設定されていない可能性がります。「/inquiry_setting」を実行してお問い合わせ先ユーザーを設定してください。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
        await ctx.respond(embed=inquiry_bad_embed)
    else:
        #確認のembedを送信
        inquiry_setting_embed=discord.Embed(title='～お問い合わせ（設定変更）～',description='お問い合わせ先のユーザーを以下のユーザーに変更します。',color=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
        inquiry_setting_embed.add_field(name='ユーザー名',value=who.mention,inline=True)
        inquiry_setting_embed.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=True)
        inquiry_setting_embed.add_field(name='ユーザーID',value=who.id,inline=False)
        inquiry_setting_embed.add_field(name='サーバーID（ギルドID）',value=guild_id,inline=True)
        inquiry_setting_embed.set_thumbnail(url=who.avatar)
        #サーバー画像の設定有無判定
        try:
            server_icon = ctx.guild.icon
            inquiry_setting_embed.set_footer(text=ctx.guild.name,icon_url=server_icon)
            await ctx.respond(embed=inquiry_setting_embed)
        except:
            inquiry_setting_embed.set_footer(text=ctx.guild.name)
            await ctx.respond(embed=inquiry_setting_embed)

@bot.slash_command(name='inquiry_send',description='このコマンドではサーバー管理者にお問い合わせすることができます。',guild_ids=[807953798894714960])
async def slash_command_inquirysend(ctx,send_content):
    guild_id=ctx.guild.id
    user_id=ctx.user.id
    user=bot.get_user(id_db.inquiry_return(guild=guild_id))
    server_name=ctx.guild.name
    inquiry_number = id_db.inquiry_num_set(guild=guild_id,user=user_id,content=send_content)
    try:
        #↓「inquiry_setting」の設定したユーザに対してのembed
        inq_ad_res=discord.Embed(title='～お問い合わせ～',description=f'{server_name}のサーバーにてお問い合わせがありました。内容は以下の通りです。返信する際はお問い合わせ番号を「/inquiry_reply」のnumber引数に入力してください。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
        inq_ad_res.add_field(name='お問い合わせ内容',value=send_content,inline=False)
        inq_ad_res.add_field(name='送信者',value=user.mention,inline=True)
        inq_ad_res.add_field(name='送信元サーバー',value=server_name,inline=False)
        inq_ad_res.add_field(name='お問い合わせ番号',value=inquiry_number,inline=True)
        await user.send(embed=inq_ad_res)
        #↓送信元のサーバに確認用のembed
        inq_check_embed=discord.Embed(title='～お問い合わせ（通知）～',description='お問い合わせが完了しました。返信をお待ちください。',color=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
        inq_check_embed.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=True)
        inq_check_embed.add_field(name='お問い合わせ番号',value=inquiry_number,inline=True)
        #サーバー画像の設定有無判定
        try:
            server_icon = ctx.guild.icon
            inq_check_embed.set_footer(text=ctx.guild.name,icon_url=server_icon)
            await ctx.respond(embed=inq_check_embed)
            time.sleep(10)
            await ctx.delete()
        except:
            inq_check_embed.set_footer(text=ctx.guild.name)
            await ctx.respond(embed=inq_check_embed)
            time.sleep(10)
            await ctx.delete()
    except Exception as e:
        inq_err_res=discord.Embed(title='エラーが発生しました…',description='もう一度正しく入力されているかを確認ください。')
        inq_err_res.add_field(name='エラー内容',value=e)
        await ctx.respond(embed=inq_err_res)

@bot.slash_command(name='inquiry_reply',description='お問い合わせに対対して信が可能です。')
async def inquiryreply(ctx,who:discord.Option(discord.Member,'返信相手を選択してください。',Required=True),number,send_content):
    user_id=int(who.id) #送信相手のID取得
    
    server_name=ctx.guild.name
    user = bot.get_user(user_id)
    try:
        inquiry_reply_embed = discord.Embed(title='お問い合わせ（返信）',description='お問い合わせに対して返信が返ってきました。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
        inquiry_reply_embed.add_field(name='返信内容', value=send_content,inline=False)
        inquiry_reply_embed.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=True)
        inquiry_reply_embed.add_field(name='送信者',value=user.mention,inline=True)
        inquiry_reply_embed.add_field(name='送信元サーバー',value=server_name,inline=True)
        await user.send(embed=inquiry_reply_embed)
        #↓送信元のサーバに確認用のembed
        inq_check_embed=discord.Embed(title='～お問い合わせ（通知）～',description='返信が完了しました。',color=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
        inq_check_embed.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=True)
        #サーバー画像の設定有無判定
        try:
            server_icon = ctx.guild.icon
            inq_check_embed.set_footer(text=ctx.guild.name,icon_url=server_icon)
            await ctx.respond(embed=inq_check_embed)
            time.sleep(10)
            await ctx.delete()
        except:
            inq_check_embed.set_footer(text=ctx.guild.name)
            await ctx.respond(embed=inq_check_embed)
            time.sleep(10)
            await ctx.delete()
    except Exception as e:
        inq_err_res=discord.Embed(title='エラーが発生しました…',description='もう一度正しく入力されているかを確認ください。')
        inq_err_res.add_field(name='エラー内容',value=e)
        await ctx.respond(embed=inq_err_res)


bot.remove_command('help')

bot.run(discord_token.token())