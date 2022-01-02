from asyncio.windows_events import NULL
import sqlite3
import os
import re
import random
import string

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
        return False

def inquiry_return(guild) -> int:
    cur = conn.cursor()
    cur.execute('select * from inquiry_id where guild_id=?',(guild,))
    inq_return=str(cur.fetchall()).replace("[(None,","").replace(")]","")
    inq_return=re.search(",.*",inq_return)
    inq_return=inq_return.group()
    inq_return=inq_return.replace(",","")
    conn.commit()
    cur.close()
    return int(inq_return)

def inquiry_update(guild,user)-> None or False:
    cur = conn.cursor()
    cur.execute('select * from inquiry_id where guild_id=?',(guild,))
    if cur.fetchall() != []:
        cur.execute('update inquiry_id set user_id=? where guild_id=?',(user,guild))
        conn.commit()
        cur.close()
        return None
    else:
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

#create table channel_id(id int primary key,channel1,channel2); 
def forwarding_channel_set(channel1,channel2)-> None:
    cur = conn.cursor()
    cur.execute('insert into channel_id(channel1, channel2) values(?,?)',(channel1,channel2,))
    conn.commit()
    cur.close()
    return None

def forwarding_channel_return()-> int:
    cur = conn.cursor()
    cur.execute('select * from url')
    conn.commit()
    cur.close()
    return int()