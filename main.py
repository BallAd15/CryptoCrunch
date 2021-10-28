import os
import websocket #pip install websocket-client
import json
import threading
import time
import requests
import emoji

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

def add_reaction(emoji,message_id):
  headers={
    'authorization':os.getenv('token')
    }
  r=requests.put(f'https://discord.com/api/v9/channels/699702250531979325/messages/{message_id}/reactions/{emoji}/%40me',headers=headers)



ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = recieve_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

token = os.getenv('token')
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
      #guild_id=int(event['d']['guild_id'])
      author_id=int(event['d']['author']['id'])

      if channel_id==699702250531979325 and author_id==617037497574359050:

        restricted_ids=['194114491552628737','258297161740058624','903314702728319056',]

        #print(f"{event['d']['author']['username']}: {event['d']['content']}")

        string=str({event['d']['embeds'][0]['description']})

        name_end=string.find("left a")

        name=string[4:(name_end-2)]
        if name in restricted_ids:
          break
        
        time.sleep(2)
        index = string.find('React w')

        emojic = string[index+11:index+12]
        msgid = int(event['d']['id'])


        add_reaction(emojic, msgid)
      op_code = event['op']

      if op_code == 11:
        print('heartbeat received')

    except:
        pass
