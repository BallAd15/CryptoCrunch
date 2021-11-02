import os
import discord
from discord import Permissions
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import requests
import asyncio
import aiohttp
import random
import json
import threading
import websocket
import time
#ok
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = 's.',intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  await client.change_presence(status = discord.Status.online,activity=discord.Activity(type=discord.ActivityType.watching, name='Otaku Service'))
  
  
def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print('Heartbeat begin')
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat sent")

def add_reaction(emoji,message_id, channel_id):
  #one_of=['NDMyNzE0MzE3NDU3MjYwNTY1.YXutiQ.LRhMARDU2RZIPMVgTiHSZEqFP-Q']#'NzcyNzc4NTM1NzA5NDQyMDc4.YXv1Vw.o-GYGwoPNuWRie-v9IZfTFKyZGA'
  #auth_random=random.choice(one_of)
  headers={
    'authorization':'NTg1OTE0NDI5NzQ1NTI4ODUz.YYAsdg.Rb1pYVf6GQ9DrkEdSfJt0mrAs38'
    }
  r=requests.put(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/%40me',headers=headers)
  time.sleep(0.8)
  r=requests.delete(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/%40me',headers=headers)

ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = recieve_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

token = "NTg1OTE0NDI5NzQ1NTI4ODUz.YYAsdg.Rb1pYVf6GQ9DrkEdSfJt0mrAs38"
payload = {
    'op': 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": 'pc'
        }
    }
}
send_json_request(ws, payload)

while True:
  event = recieve_json_response(ws)
  try:
    channel_id=int(event['d']['channel_id'])
    guild_id=int(event['d']['guild_id'])
    author_id=int(event['d']['author']['id'])

    if author_id==617037497574359050:
      restricted_ids=['194114491552628737','258297161740058624','903314702728319056']

      #print(f"{event['d']['author']['username']}: {event['d']['content']}")

      string=str({event['d']['embeds'][0]['description']})
      
      find_dol=int(string.find('xa0$'))
      find_end=int(string[find_dol+4:].find(').'))
      price =float(string[find_dol+4:find_end+find_dol+4])
      
      if guild_id==846854226952978452:
        '''
        cur_begin=string.find("897155100819202088> **")
        cur_end=string.find("USELESS** (≈")
        
        amount=int(string[cur_begin+22:cur_end].replace(',', '')) 
        '''
        msgid = int(event['d']['id'])
        

        if price>5.1:
          #if channel_id==900880235086626846:
          cased_auth=["NzcyNzc4NTM1NzA5NDQyMDc4.YX1qMg.WgLf3GjxJWjjJrqdeRjr12yKDx8","NTg1OTE0NDI5NzQ1NTI4ODUz.YYAsdg.Rb1pYVf6GQ9DrkEdSfJt0mrAs38"]
          time.sleep(1.7)
          for j in cased_auth:
            header={'authorization': j}
            index = string.find('React w')
            emoji = string[index+11:index+12]
            r=requests.put(f'https://discord.com/api/v9/channels/{channel_id}/messages/{msgid}/reactions/{emoji}/%40me',headers=header)
            time.sleep(1)
            r=requests.delete(f'https://discord.com/api/v9/channels/{channel_id}/messages/{msgid}/reactions/{emoji}/%40me',headers=header)
        continue
      
      name_end=string.find("left a")
      
      name=string[4:(name_end-2)]
      if name in restricted_ids:
          continue
          
      if price>0.03:
        time.sleep(1.8)
        index = string.find('React w')

        emojic = string[index+11:index+12]
        msgid = int(event['d']['id'])


        add_reaction(emojic, msgid,channel_id)

      op_code = event['op']
      if op_code == 11:
          print('heartbeat received')
  except:
    pass 
