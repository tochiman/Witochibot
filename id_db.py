from asyncio.windows_events import NULL
import sqlite3
import os
import re
import random
import string

from discord import channel

os.chdir("C:/Users/yuuto/OneDrive/VS_code/python/Witochibot")

dbname = 'id.db'
conn = sqlite3.connect(dbname)

#create table inquiry_id(id int primary key,guild_id int unique,user_id int unique);
def inquiry_set(guild,user) -> None or False:
    cur = conn.cursor()
    try:
        cur.execute('insert into inquiry_id(guild_id,user_id) values(?,?)',(guild,user,))
        conn.commit()
        cur.close()
        return None
    except:
        cur.close()
        return False

def inquiry_return(guild) -> int or False:
    try:
        cur = conn.cursor()
        cur.execute('select * from inquiry_id where guild_id=?',(guild,))
        inq_return=str(cur.fetchall()).replace("[(None,","").replace(")]","")
        inq_return=re.search(",.*",inq_return)
        inq_return=inq_return.group()
        inq_return=inq_return.replace(",","")
        conn.commit()
        cur.close()
        return int(inq_return)
    except:
        cur.close()
        return False

def inquiry_update(guild,user)-> None or False:
    cur = conn.cursor()
    cur.execute('select * from inquiry_id where guild_id=?',(guild,))
    if cur.fetchall() != []:
        cur.execute('update inquiry_id set user_id=? where guild_id=?',(user,guild))
        conn.commit()
        cur.close()
        return None
    else:
        cur.close()
        return False

# create table tweet_channel(guild_id int unique, channel_id int);
def tweet_set_channel(guild,channel) -> None or False:
    cur = conn.cursor()
    try:
        cur.execute('insert into tweet_channel(guild_id,channel_id) values(?,?)',(guild,channel,))
        conn.commit()
        cur.close()
        return None
    except:
        return False

'''
#create table inquiry_num(guild_id int,user_id int,number int unique, inquiry_content string);
def inquiry_num_set(guild,user,content) -> str:
    cur = conn.cursor()
    while True:
        try:
            inquiry_num = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits for _ in range(4)))
            cur.execute('insert into inquiry_num(guild_id,user_id,number,inquiry_content) value(?,?,?,?)',(guild,user,inquiry_num,content))
            break
        except:
            pass
    conn.commit()
    cur.close()
    return str(inquiry_num)

def inquiry_num_return(guild,user,number):
    cur = conn.cursor()
    cur.execute('')
    conn.commit()
    cur.close()
'''

#create table channel_id(guild_id1 int unique, guild_id2 int unique,channel1 int unique, channel2 int unique );
def forwarding_channel_set(guild1,guild2,channel1,channel2)-> None or False:
    cur = conn.cursor()
    try:
        cur.execute('insert into channel_id(guild_id1,guild_id2,channel1, channel2) values(?,?,?,?)',(guild1,guild2,channel1,channel2,))
        conn.commit()
        cur.close()
        return None
    except:
        cur.close()
        return False

def forwarding_channel_return(guild)-> int:
    cur = conn.cursor()
    cur.execute('select * from channel_id where guild_id1=? or guild_id2=?',(guild,guild))
    channel_return_id = str(cur.fetchall()).replace(f"({guild}","")
    channel_return_1 = re.match("\[,.+,",channel_return_id)
    channel_return_1 = channel_return_1.group().replace("[","").replace(",","")
    channel_return_2 = channel_return_id.replace("[,","").replace(f"{channel_return_1},","").replace(")]","")
    conn.commit()
    cur.close()
    return int(channel_return_1),int(channel_return_2)

def forwarding_channel_del(channel1,channel2) -> None:
    try:
        cur = conn.cursor()
        cur.execute('delete from channel_id where channel1=? and channel2=?',(channel1,channel2,))
        conn.commit()
        cur.close()
        return None
    except:
        cur.close()
        return False

