import sqlite3
import os

os.chdir("C:/Users/yuuto/OneDrive/VS_code/python/Witochibot")

dbname = 'id.db'
conn = sqlite3.connect(dbname)

#create table inquiry_id(id int primary key,guild_id int, user_id int);
def inquiry_set(guild,user):
    cur = conn.cursor()
    cur.execute('insert into inquiry_id(guild_id,user_id) values(?,?)',(guild,user,))
    conn.commit()
    cur.close()

def inquiry_return(guild):
    cur = conn.cursor()
    print(cur.execute('select * from inquiry_id where guild_id=?',(guild)))
    conn.commit()
    cur.close()

'''
def forwarding_channel_set(channel1,channel2):
    #create table channel_id(id int primary key,channel1,channel2); 
    db_name = 'main.db'
    db_connect = sqlite3.connect(db_name)
    cur = sqlite3.Cursor(db_connect)
    cur.execute('insert into channel_id(channel1, channel2) values(?,?)',(channel1,channel2,))

def forwarding_channel_return():
    #create table channel_id(id int primary key,channel1,channel2); 
    db_name = 'main.db'
    db_connect = sqlite3.connect(db_name)
    cur = sqlite3.Cursor(db_connect)
    cur.execute('select * from url')
'''
