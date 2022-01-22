#call module
import asyncio
import datetime
import json
import os
import re
import sqlite3
import string
import time
from fileinput import filename
from os import name
from random import choice, choices, random
from typing import DefaultDict
from unittest import result

import discord
from discord import client, guild, message
from discord.client import Client
from discord.ext import commands
from discord.ext.commands import MissingPermissions, context, has_permissions
from discord.ext.commands.core import check, command
from discord.member import Member
from discord.state import ConnectionState
from discord_slash import SlashCommand, SlashContext
from discord_slash.dpy_overrides import send_message
from discord_slash.utils import manage_commands
from numpy import result_type

import discord_token
import id_db
import tw

bot=commands.Bot(command_prefix='/',
                description='test',
                intents = discord.Intents.all(),
                help_command=None,
                activity=discord.Game("test") 
)
client = discord.Client()

#ランダムなrgb値返す関数
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
    #guild_id = message.guild.id
    #ch_return = id_db.forwarding_channel_return(guild=guild_id)
    #channel1 = int(ch_return[0])
    #channel2 = int(ch_return[1])
    match_id = message.channel.id
    #print(channel1)
    #print(channel2)
    channel1 = 925429318904070165
    channel2 = 930109776568942624
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

    if match_id == channel1:
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

    elif match_id == channel2:
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
        
    else:
        pass

    await bot.process_commands(message) #on_message と commandsの共存させる

'''
@bot.slash_command(name="channel_setup", description="このコマンドはメッセージを別のサーバーへ転送するチャンネルを設定するものです。（※管理者権限がないと実行できません）", guild_ids=[807953798894714960])
@commands.has_permissions(administrator = True)
async def ch_setup(ctx, channel1:discord.Option(discord.TextChannel, "チャンネルを選択してください", required=True), channel2:discord.Option(discord.TextChannel,'チャンネルを選択してください',required=True)):#, default=None, choices=["1","2","いっぱい"]
    send_author_channel_id = ctx.channel.id  #送信者のチャンネルID取得
    send_author_channel_id = bot.get_channel(send_author_channel_id)
    Channel1_ID = channel1.id               #送信元のIDを変数に格納
    Channel2_ID = channel2.id               #送信先のIDを変数に格納
    Channel1_name = channel1.name
    Channel2_name = channel2.name
    guild_id = ctx.guild.id
    check_db = id_db.forwarding_channel_set(guild=guild_id,channel1=Channel1_ID,channel2=Channel2_ID)
    if check_db == False:
        bad_embed=discord.Embed(title='～メッセージ転送（設定エラー）～',description='チャンネルが既に設定されている可能性があります。（片方が既に設定されている場合は設定することができません）別のチャンネルを設定してください。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
        await ctx.respond(embed=bad_embed)
    else:
        #セットアップの確認情報のEmbed
        channel_setup_embed = discord.Embed(title='メッセージ転送（設定）',description='メッセージを転送するチャンネルを以下のように設定しました。',colour=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
        channel_setup_embed.insert_field_at(0,name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=True)
        channel_setup_embed.insert_field_at(2,name='Channel1 name',value=Channel1_name,inline=True)
        channel_setup_embed.insert_field_at(2,name='Channel2 name',value=Channel2_name,inline=True)
        channel_setup_embed.insert_field_at(1,name='Channel2 ID',value=Channel2_ID,inline=True)
        channel_setup_embed.insert_field_at(1,name='Channel1 ID',value=Channel1_ID,inline=True)
        #サーバー画像の設定有無判定
        try:
            server_icon = ctx.guild.icon
            server_name = ctx.guild.name
            channel_setup_embed.set_footer(text=server_name,icon_url=server_icon)
            await ctx.respond(embed=channel_setup_embed)
        except:
            channel_setup_embed.set_footer(text=ctx.guild.name)
            await ctx.respond(embed=channel_setup_embed)

@bot.slash_command(name='channel_delete',description='このコマンドではメッセージ転送をするように設定したチャンネルを通常のチャンネルに変更します。（※管理者権限がないと実行できません）', guild_ids=[807953798894714960])
@commands.has_permissions(administrator = True)
async def ch_del(ctx,channel1:discord.Option(discord.TextChannel,'チャンネルを選択してください。',Required=True),channel2:discord.Option(discord.TextChannel,'チャンネルを選択してください。',Required=True)):
    channel1_id = channel1.id
    channel2_id = channel2.id
    Channel1_name = channel1.name
    Channel2_name = channel2.name
    delete_check = id_db.forwarding_channel_del(channel1=channel1_id,channel2=channel2_id)
    if delete_check == False:
        bad_embed=discord.Embed(title='～メッセージ転送（解除エラー）～',description='設定を削除しようとしたチャンネルがもともと設定されていなかった可能性があります。正しく入力されているかを確認してください。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
        await ctx.respond(embed=bad_embed)
    else:
        channel_delete_embed=discord.Embed(title='メッセージ転送（解除）',description='以下のチャンネルのメッセージ転送機能の解除に成功しました。',color=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
        channel_delete_embed.insert_field_at(0,name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=True)
        channel_delete_embed.insert_field_at(2,name='Channel1 name',value=Channel1_name,inline=True)
        channel_delete_embed.insert_field_at(2,name='Channel2 name',value=Channel2_name,inline=True)
        channel_delete_embed.insert_field_at(1,name='Channel2 ID',value=channel2_id,inline=True)
        channel_delete_embed.insert_field_at(1,name='Channel1 ID',value=channel1_id,inline=True)
        #サーバー画像の設定有無判定
        try:
            server_icon = ctx.guild.icon
            server_name = ctx.guild.name
            channel_delete_embed.set_footer(text=server_name,icon_url=server_icon)
            await ctx.respond(embed=channel_delete_embed)
        except:
            channel_delete_embed.set_footer(text=ctx.guild.name)
            await ctx.respond(embed=channel_delete_embed)
'''

@bot.slash_command(name='inquiry_setting',description='このコマンドはお問い合わせ先のユーザーを誰にするか決めることができます。（※管理者権限がないと実行できません）', guild_ids=[807953798894714960])
@commands.has_permissions(administrator = True)
async def slash_command_inquirysetting(ctx,who:discord.Option(discord.Member,'お問い合わせ先のユーザーを誰にするか選択してください',Required=True)):
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
            server_name = ctx.guild.name
            inquiry_setting_embed.set_footer(text=server_name,icon_url=server_icon)
            await ctx.respond(embed=inquiry_setting_embed)
        except:
            inquiry_setting_embed.set_footer(text=ctx.guild.name)
            await ctx.respond(embed=inquiry_setting_embed)

@bot.slash_command(name='inquiry_update',description='このコマンドではお問い合わせユーザーの変更を変更します。（※管理者権限がないと実行できません）', guild_ids=[807953798894714960])
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
            server_name = ctx.guild.name
            inquiry_setting_embed.set_footer(text=server_name,icon_url=server_icon)
            await ctx.respond(embed=inquiry_setting_embed)
        except:
            inquiry_setting_embed.set_footer(text=ctx.guild.name)
            await ctx.respond(embed=inquiry_setting_embed)

@bot.slash_command(name='inquiry_send',description='このコマンドはサーバー管理者にお問い合わせすることができます。', guild_ids=[807953798894714960])
async def slash_command_inquirysend(ctx,send_content:discord.Option(str,'お問い合わせ内容をお書きください。',required=True)):
    guild_id=ctx.guild.id
    user_id=ctx.user.id
    user=bot.get_user(id_db.inquiry_return(guild=guild_id))
    server_name=ctx.guild.name
    #inquiry_number = id_db.inquiry_num_set(guild=guild_id,user=user_id,content=send_content)
    if user != False:
        try:
            #↓「inquiry_setting」の設定したユーザに対してのembed
            inq_ad_res=discord.Embed(title='～お問い合わせ～',description=f'{server_name}のサーバーにてお問い合わせがありました。内容は以下の通りです。返信する際はお問い合わせ番号を「/inquiry_reply」のnumber引数に入力してください。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
            inq_ad_res.add_field(name='お問い合わせ内容',value=send_content,inline=False)
            inq_ad_res.add_field(name='送信者',value=ctx.author.mention,inline=True)
            try:
                server_icon = ctx.guild.icon
                server_name = ctx.guild.name
                inq_ad_res.set_footer(text=server_name,icon_url=server_icon)
                await user.send(embed=inq_ad_res)
            except:
                inq_ad_res.set_footer(text=ctx.guild.name)
                await user.send(embed=inq_ad_res)
            
            #inq_ad_res.add_field(name='お問い合わせ番号',value=inquiry_number,inline=True)

            #↓送信元のサーバに確認用のembed
            inq_check_embed=discord.Embed(title='～お問い合わせ（通知）～',description='お問い合わせが完了しました。返信をお待ちください。',color=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
            inq_check_embed.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=True)
            
            #inq_check_embed.add_field(name='お問い合わせ番号',value=inquiry_number,inline=True)

            #サーバー画像の設定有無判定
            try:
                server_icon = ctx.guild.icon
                server_name = ctx.guild.name
                inq_check_embed.set_footer(text=server_name,icon_url=server_icon)
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

    else:
        inq_err_res=discord.Embed(title='エラーが発生しました…',description='もう一度正しく入力されているかを確認ください。')
        await ctx.respond(embed=inq_err_res)

@bot.slash_command(name='inquiry_reply',description='お問い合わせに対対して返信が可能です。（※管理者権限がないと実行できません）', guild_ids=[807953798894714960])
@commands.bot_has_permissions(administrator=True)
async def inquiryreply(ctx,who:discord.Option(discord.Member,'返信相手を選択してください。',Required=True),send_content:discord.Option(str,'お問い合わせ内容をお書きください。',required=True)):
    user_id=int(who.id) #送信相手のID取得
    server_name=ctx.guild.name
    user = bot.get_user(user_id)

    try:
        inquiry_reply_embed = discord.Embed(title='お問い合わせ（返信）',description='お問い合わせに対して返信が返ってきました。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
        inquiry_reply_embed.add_field(name='返信内容', value=send_content,inline=False)
        inquiry_reply_embed.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=True)
        inquiry_reply_embed.add_field(name='送信者',value=ctx.author.mention,inline=True)
        try:
            server_icon = ctx.guild.icon
            server_name= ctx.guild.name
            inquiry_reply_embed.set_footer(text=server_name,icon_url=server_icon)
            await user.send(embed=inquiry_reply_embed)
        except:
            inquiry_reply_embed.set_footer(text=ctx.guild.name)
            await user.send(embed=inquiry_reply_embed)

        #↓送信元のサーバに確認用のembed
        inq_check_embed=discord.Embed(title='～お問い合わせ（通知）～',description='返信が完了しました。',color=discord.Colour.from_rgb(int(rgb_result[0]),int(rgb_result[1]),int(rgb_result[2])))
        inq_check_embed.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=True)
        #サーバー画像の設定有無判定
        try:
            server_icon = ctx.guild.icon
            server_name = ctx.guild.name
            inq_check_embed.set_footer(text=server_name,icon_url=server_icon)
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

@bot.slash_command(name='inquiry_check',description='このコマンドはお問い合わせ先のユーザーを確認することができます。', guild_ids=[807953798894714960])
async def inquirycheck(ctx):
    guild_id = ctx.guild.id
    user_id=id_db.inquiry_return(guild=guild_id)
    user=bot.get_user(user_id)

    inq_check_embed = discord.Embed(title='お問い合わせ（確認）',description='現在このサーバーで登録されているお問い合わせ先ユーザーは以下の通りです。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
    inq_check_embed.add_field(name='登録者名',value=user.name,inline=True)
    inq_check_embed.add_field(name='送信時間',value=f'{now:%Y-%m-%d %H:%M:%S}',inline=True)
    await ctx.respond(embed=inq_check_embed)

@bot.slash_command(name='server',description='このコマンドはサーバーの管理をするものです。（※管理者権限がないと実行できません）',hidden=True, guild_ids=[807953798894714960])
@commands.bot_has_permissions(ban_members = True)
@commands.bot_has_permissions(administrator=True)
async def server(ctx, what : discord.Option(str, '何を実行しますか。', choices=["kick", "BAN", "UnBAN"], required=True),do : discord.Option(discord.Member, 'だれに実行しますか？(what引数がUnBAN以外の場合は必要になります)', required=False), reason : discord.Option(str, 'ここでは監査ログの理由欄に記載される理由を書いてください。（相手先にも表示されます）（任意）', required=False),option : discord.Option(str,'オプション引数。（UnBANしたい場合ここに名前を入れてください)',required=False)):
    try:
        #do_argがある場合の条件
        if do != '':
            if what == 'kick':
                user_id = int(do.id) #ユーザーID取得
                user = bot.get_user(user_id)
                kick_embed = discord.Embed(title='あなたはサーバーからキックされました。')
                kick_embed.add_field(name='キックされたサーバー',value=ctx.guild.name,inline=False)
                kick_embed.add_field(name='理由',value=reason)
                await user.send(embed=kick_embed)

                await do.kick(reason=reason) #kick実行

                kick_exe_embed = discord.Embed(title='サーバー管理（kick）',description='以下のユーザーをサーバーからキックしました。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
                kick_exe_embed.add_field(name='kickした人',value=do.mention,inline=True)
                kick_exe_embed.add_field(name='理由',value=reason)
                kick_exe_embed.add_field(name='送信時間',value=f'{now:%Y-%m-%d %H:%M:%S}',inline=False)
                kick_exe_embed.set_thumbnail(url=user.avatar)
                #サーバー画像の設定有無判定
                try:
                    server_icon = ctx.guild.icon
                    server_name = ctx.guild.name
                    kick_exe_embed.set_footer(text=server_name,icon_url=server_icon)
                    await ctx.respond(embed=kick_exe_embed)
                except:
                    kick_exe_embed.set_footer(text=ctx.guild.name)
                    await ctx.respond(embed=kick_exe_embed)

            elif what == 'BAN':
                user_id = do.id #ユーザーID取得
                user=bot.get_user(user_id)
                ban_embed = discord.Embed(title='あなたはサーバーからBANされました。')
                ban_embed.add_field(name='BANされたサーバー',value=ctx.guild.name,inline=False)
                ban_embed.add_field(name='理由',value=reason)
                await user.send(embed=ban_embed)
                
                await do.ban(reason=reason) #ban実行

                ban_exe_embed = discord.Embed(title='サーバー管理（BAN）',description='以下のユーザーをサーバーからBANしました。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
                ban_exe_embed.add_field(name='BANされた人',value=do.mention,inline=True)
                ban_exe_embed.add_field(name='理由',value=reason)
                ban_exe_embed.add_field(name='送信時間',value=f'{now:%Y-%m-%d %H:%M:%S}',inline=False)
                ban_exe_embed.set_thumbnail(url=user.avatar)
                #サーバー画像の設定有無判定
                try:
                    server_icon = ctx.guild.icon
                    server_name = ctx.guild.name
                    ban_exe_embed.set_footer(text=server_name,icon_url=server_icon)
                    await ctx.respond(embed=ban_exe_embed)
                except:
                    ban_exe_embed.set_footer(text=ctx.guild.name)
                    await ctx.respond(embed=ban_exe_embed)
        #do_argがなにもない場合の条件
        if option != '':
            if what == 'UnBAN': 
                #banする人をguildから取得しidのみを摘出する。
                bans=await ctx.guild.bans()
                unban_list = str(["{0.id} {0.name}".format(entry.user) for entry in bans])
                unban_list = re.search(f".*{option}",unban_list)
                unban_str = str(unban_list.group())
                unban_int = int(unban_str.replace("['","").replace(f"{option}",""))
                user = await bot.fetch_user(unban_int)
                await ctx.guild.unban(user)

                user_embed = bot.get_user(unban_int)
                unban_exe_embed=discord.Embed(title="サーバー管理（UnBAN)", description='以下のユーザーのBANを解除しました。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
                unban_exe_embed.set_thumbnail(url=user_embed.avatar)
                unban_exe_embed.add_field(name="UnBANされた人", value=user_embed.display_name, inline=False)
                unban_exe_embed.add_field(name='理由',value=reason)
                unban_exe_embed.add_field(name='送信時間',value=f'{now:%Y-%m-%d %H:%M:%S}',inline=False)
                #サーバー画像の設定有無判定
                try:
                    server_icon = ctx.guild.icon
                    server_name = ctx.guild.name
                    unban_exe_embed.set_footer(text=server_name,icon_url=server_icon)
                    await ctx.respond(embed=unban_exe_embed)
                except:
                    unban_exe_embed.set_footer(text=ctx.guild.name)
                    await ctx.respond(embed=unban_exe_embed)
    except:
        import traceback
        print(traceback.print_exc())
        server_err_embed = discord.Embed(title='サーバー管理（エラー）', description='サーバー管理コマンドを実行することができませんでした。正しく入力されているかを確認してください。', color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
        #サーバー画像の設定有無判定
        try:
            server_icon = ctx.guild.icon
            server_name = ctx.guild.name
            server_err_embed.set_footer(text=server_name,icon_url=server_icon)
            await ctx.respond(embed=server_err_embed)
        except:
            server_err_embed.set_footer(text=ctx.guild.name)
            await ctx.respond(embed=server_err_embed)

@bot.slash_command(name='developer',description='botの開発者にコマンド等の希望・要望を提出することができます。')
@commands.dm_only()
async def inquiry(ctx,content : discord.Option(str,'お問い合わせ内容をお書きください。',required=True)):
    dev_tochiman = int(536888269393362954)
    user = bot.get_user(dev_tochiman)
    inquiry_embed = discord.Embed(title='開発者への要望・希望',description='botの開発者に対して、要望・希望を以下の内容で送信しました。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
    inquiry_embed.add_field(name='送信内容',value=content,inline=True)
    inquiry_embed.add_field(name='送信時間',value=f'{now:%Y-%m-%d %H:%M:%S}',inline=False)
    await user.send(embed=inquiry_embed)

    #送信したことを知らせる
    await ctx.respond(f'{ctx.author.mention}さん！ありがとうございます！')
    time.sleep(3)
    await ctx.delete()

@bot.slash_command(name='help',description='コマンドの使い方を確認することができます。', guild_ids=[807953798894714960])
async def help(ctx):
    #送信者のidを取得
    user_id = ctx.author.id
    user =bot.get_user(user_id)
    #ヘルプについてのEmbed
    with open(r'C:\Users\yuuto\OneDrive\VS_code\python\Witochibot\help_page.html', 'rb') as f:
        await ctx.respond(file=discord.File(f,filename='help_page.html'))

@bot.slash_command(name='tweet_setting',description='「tweet_get」コマンドで指定したtwitterアカウントの画像付きツイートを送信するチャンネルを指定します。（※管理者権限がないと実行できません）',guild_ids=[807953798894714960])
@commands.has_permissions(administrator=True)
async def tweet_setting(ctx,channel : discord.Option(discord.TextChannel,'送信するチャンネルを指定してください。',required=True)):
    #id取得
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    #指定されたチャンネルid取得
    channel_id = channel.id

    #dbにコミット
    check_db = id_db.tweet_set_channel(guild=guild_id,channel=channel_id)

    if check_db == False:
        bad_embed=discord.Embed(title='～チャンネル設定エラー～',description='１つのサーバーに１つまでしかチャンネルを指定することができません。または、指定されたチャンネルが正しく入力されているかを確認してください。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
        await ctx.respond(embed=bad_embed)
    else:
        # 確認のembed送信
        check_embed = discord.Embed(title='チャンネル設定',description='画像付きのツイートを送信するチャンネルを以下の場所にします。',color=discord.Colour.from_rgb(r=int(rgb_result[0]),g=int(rgb_result[1]),b=int(rgb_result[2])))
        check_embed.add_field(name='送信先チャンネル名',value=channel.name,inline=True)
        check_embed.add_field(name='送信先チャンネルID',value=channel_id,inline=True)
        check_embed.add_field(name='送信時間',value=f"{now:%Y-%m-%d %H:%M:%S}",inline=True)
        #サーバー画像の設定有無判定
        try:
            server_icon = ctx.guild.icon
            server_name = ctx.guild.name
            check_embed.set_footer(text=server_name,icon_url=server_icon)
            await ctx.respond(embed=check_embed)
        except:
            check_embed.set_footer(text=ctx.guild.name)
            await ctx.respond(embed=check_embed)


bot.remove_command('help')
bot.run(discord_token.token())
