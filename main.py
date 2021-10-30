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
  
  cased_auth="NzcyNzc4NTM1NzA5NDQyMDc4.YX1qMg.WgLf3GjxJWjjJrqdeRjr12yKDx8"
  if channel_id==900880235086626846:
    header={'authorization': cased_auth}
    r=requests.put(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/%40me',headers=header)
  
  headers={
    'authorization':'NDMyNzE0MzE3NDU3MjYwNTY1.YX1yUQ.vysr58-D4boTy66_0OwWaIVtIzs'
    }
  r=requests.put(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/%40me',headers=headers)
  time.sleep(0.8)
  r=requests.delete(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/%40me',headers=headers)

ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = recieve_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

token = "NDMyNzE0MzE3NDU3MjYwNTY1.YX1yUQ.vysr58-D4boTy66_0OwWaIVtIzs"
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

    if author_id==617037497574359050:
      restricted_ids=['194114491552628737','258297161740058624','903314702728319056']

      #print(f"{event['d']['author']['username']}: {event['d']['content']}")

      string=str({event['d']['embeds'][0]['description']})

      name_end=string.find("left a")

      name=string[4:(name_end-2)]
      if name in restricted_ids:
          break
          
      time.sleep(1.4)
      index = string.find('React w')

      emojic = string[index+11:index+12]
      msgid = int(event['d']['id'])


      add_reaction(emojic, msgid,channel_id)
      print("Reacted")
      op_code = event['op']
      if op_code == 11:
          print('heartbeat received')
  except:
    pass 

  
@client.command()
async def leave(ctx):
  to_leave = client.get_guild(807116277029273630) 
  await to_leave.leave()

#Servers bot is in
@client.command()
async def where(ctx):
   if ctx.message.author.id == 772778535709442078:
     s=""
     for guild in client.guilds:
       s+=f"*{guild}*\n ID => {guild.id}\n Owner => {guild.owner}\n\n"
     await ctx.send(s)

#Custom Help
@client.group(invoke_without_command=True)
@commands.cooldown(1,7,commands.BucketType.user)
async def help(ctx):
  
  em = discord.Embed(title="🐱‍👓 Help", description = "```md\nSenpai greets you! :)```", color = 0x15b9d3) #color = ctx.author.color
  
  em.add_field(name='⚙️ General Commands\n\n', value = 
  """```css\n
  s.anime <name>   -   Anime search
  s.manga <name>   -   Manga search
  s.ch <character>  -  Search by character
  s.hentai - Sends hentai 
  s.yt <query> - Search Youtube
  ```
  """, inline = False) #b.toggle <role>   -   Underwork 
  '''
  em.add_field(name='📑 Info Commands\n\n', value = 
  """```css\n
  b.quote   -   Generates random quotes
  b.wiki <query>   -   Search the wikipedia
  b.define <query> - Returns definitions of query.
  b.server - Display server info```
   """, inline = False)

  em.add_field(name='🃏 Fun Commands\n\n', value = 
  """```css\n
  b.tictactoe <p1><p2> - TicTacToe game
  b.akash <help>   -   Cave exclusive 
  b.a <message>   -   AI command, Chat with the bot.
  b.kick <member> - Generates custom kicking image.
  b.kiss <member> - Generates custom kissing image.
  b.gotem - Places your pfp over internet roast guy.```
   """, inline = False)
  '''
  em.set_footer(icon_url = client.user.avatar_url, text = f"Presented by Senpai")
  
  await ctx.send(embed=em)

#Query
def SearchByTitle():
    query = '''
    query($search: String, $type: MediaType) {
        Media(search: $search, type: $type) {
        title
        {
            romaji
            english
        }
        siteUrl
        type
        format
        genres
        status
        episodes
        duration
        status
        description(asHtml: true)
        coverImage {
            large
        }
        season
        seasonYear
        startDate {
            day
            month
            year
        }
        averageScore
        favourites
        studios
        {
            edges
            {
                node
                {
                    name
                }
            }
        }
        chapters
        volumes
        hashtag
        }
}
    '''
    return query
def SearchByID():
    query = '''
    query($id: Int, $type: MediaType) {
        Media(id: $id, type: $type) {
        title
        {
            romaji
            english
        }
        siteUrl
        type
        format
        genres
        status
        episodes
        duration
        status
        description(asHtml: true)
        coverImage {
            large
        }
        season
        seasonYear
        startDate {
            day
            month
            year
        }
        averageScore
        favourites
        studios
        {
            edges
            {
                node
                {
                    name
                }
            }
        }
        chapters
        volumes
        hashtag
        }
        }
    '''
    return query
def searchChar():
    query = '''
    query ($search: String) {
      Character(search: $search) {
        siteUrl
        name {
          full
        }
        media(perPage: 1) {
          nodes {
            title {
                romaji
                english
            }
            siteUrl
          }
        }
        image {
          large
        }
        description(asHtml: true)
      }
    }
    '''
    return query
#Variables
def GetByID(type, id):
    type = type.upper()
    if type != 'ANIME' and type != 'MANGA':
        return False
    variables = {
        'type' : type,
        'id': id
    }
    return variables
def GetByTitle(type, title):
    type = type.upper()
    if type != 'ANIME' and type != 'MANGA':
        return False
    variables = {
        'type' : type,
        'search' : title
    }
    return variables
def GetByChar(charName):
    variables = {
        'search' : charName
    }
    return variables
#query
def SearchByID():
    query = '''
    query($id: Int, $type: MediaType) {
        Media(id: $id, type: $type) {
        title
        {
            romaji
            english
        }
        siteUrl
        type
        format
        genres
        status
        episodes
        duration
        status
        description(asHtml: true)
        coverImage {
            large
        }
        season
        seasonYear
        startDate {
            day
            month
            year
        }
        averageScore
        favourites
        studios
        {
            edges
            {
                node
                {
                    name
                }
            }
        }
        chapters
        volumes
        hashtag
        }
        }
    '''
    return query
def SearchByTitle():
    query = '''
    query($search: String, $type: MediaType) {
        Media(search: $search, type: $type) {
        title
        {
            romaji
            english
        }
        siteUrl
        type
        format
        genres
        status
        episodes
        duration
        status
        description(asHtml: true)
        coverImage {
            large
        }
        season
        seasonYear
        startDate {
            day
            month
            year
        }
        averageScore
        favourites
        studios
        {
            edges
            {
                node
                {
                    name
                }
            }
        }
        chapters
        volumes
        hashtag
        }
        }
    '''
    return query
def run_query(query, variables):
    request = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
    if request.status_code == 200:
        return request.json()
    elif request.status_code == 404:
        print ("Invalid search.")
        return
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
#Misc
#Clean

def removeTags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
def cutLength(text):
    if len(text) > 900:
        return text[:900] + "..."
    return text
def replaceNone(text):
    if text is None:
        return 'N/A'
    return text


#Anime Search
def animeSearch(title):
    if title.isnumeric():
        query = SearchByID()
        variables = GetByID('anime', title)
    elif not title.isnumeric():
        query = SearchByTitle()
        variables = GetByTitle('anime', title)
    if variables:
        result = run_query(query, variables)
        if not result:
            return discord.Embed(title="🚫 Error: ",description="*{}* was not found in the database. Gomenasai!.".format(title),color=0xf1e10d)

        embed = discord.Embed(
            color=0xf1e10d,
            title=('{} ({}) {}'.format(result["data"]["Media"]["title"]["romaji"],
                                       result["data"]["Media"]["title"]["english"],
                                       result["data"]["Media"]["format"])),
            url=result["data"]["Media"]["siteUrl"],
            description=(removeTags(result["data"]["Media"]["description"])).replace("&quot;", '"')
        )
        embed.add_field(name="Status", value=result["data"]["Media"]["status"].upper(), inline=True)
        embed.add_field(name="Season",
                        value='{} {}'.format(result["data"]["Media"]["season"], result["data"]["Media"]["seasonYear"]),
                        inline=True)
        embed.add_field(name="Number of Episodes", value=result["data"]["Media"]["episodes"], inline=True)
        embed.add_field(name="Duration",
                        value='{} minutes/episode'.format(result["data"]["Media"]["duration"], inline=True))
        embed.add_field(name="Favourites", value=result["data"]["Media"]["favourites"], inline=True)
        embed.add_field(name="Average Score", value='{}%'.format(result["data"]["Media"]["averageScore"], inline=True))
        embed.set_thumbnail(url=result["data"]["Media"]["coverImage"]["large"])
        return embed
#Manga Search
def mangaSearch(title):
    if title.isnumeric():
        query = SearchByID()
        variables = GetByID('manga', title)
    elif not title.isnumeric():
        query = SearchByTitle()
        variables = GetByTitle('manga', title)
    if variables:
        result = run_query(query, variables)
        if not result:
            return discord.Embed(title = "💢Error:",description="*{}* was not found in the database, Gomenasai.".format(title),color=0xfa772f)

        embed = discord.Embed(
            colour=0xfa772f,
            title=('{} ({}) {}'.format(result["data"]["Media"]["title"]["romaji"],
                                       result["data"]["Media"]["title"]["english"],
                                       result["data"]["Media"]["format"])),
            url=result["data"]["Media"]["siteUrl"],
            description=(removeTags(result["data"]["Media"]["description"])).replace("&quot;", '"')
        )

        embed.add_field(name="Status", value=result["data"]["Media"]["status"].upper(), inline=True)
        embed.add_field(name="Start Date",
                        value='{}/{}/{}'.format(result["data"]["Media"]["startDate"]["day"],
                                                result["data"]["Media"]["startDate"]["month"],
                                                result["data"]["Media"]["startDate"]["year"]),
                        inline=True)
        embed.add_field(name="Number of Chapters", value=replaceNone(result["data"]["Media"]["chapters"]), inline=True)
        embed.add_field(name="Number of Volumes", value=replaceNone(result["data"]["Media"]["volumes"]), inline=True)
        embed.add_field(name="Favourites", value=result["data"]["Media"]["favourites"], inline=True)
        embed.add_field(name="Average Score",
                        value='{}'.format(replaceNone(result["data"]["Media"]["averageScore"]), inline=True))
        embed.set_thumbnail(url=result["data"]["Media"]["coverImage"]["large"])
        return embed
def charSearch(charName):
    query = searchChar()
    variables = GetByChar(charName)
    if variables:
        result = run_query(query, variables)
        if not result:
            return discord.Embed(title="💢 Error: ",description="*{}* was not found in the database, Gomenasai.".format(charName),color = 0xc21b1b)

        embed = discord.Embed(
            colour=0xc21b1b,
            title=result["data"]["Character"]["name"]["full"],
            url=result["data"]["Character"]["siteUrl"]
        )

        desc = cutLength(removeTags(result["data"]["Character"]["description"]).replace("&quot;", '"'))

        for title in result["data"]["Character"]["media"]["nodes"]:
            embed.add_field(name="Title of Source", value='[{} ({})]({})'.format(title["title"]["romaji"], title["title"]["english"], title["siteUrl"], inline=False))
        embed.add_field(name="Description", value=desc, inline=False)
        embed.set_thumbnail(url=result["data"]["Character"]["image"]["large"])
        return embed

#Youtube
#Youtube
async def reaction_buttons(
    ctx, message, functions, timeout=300.0, only_author=False, single_use=False, only_owner=False
):
    """
    Handler for reaction buttons
    :param message     : message to add reactions to
    :param functions   : dictionary of {emoji : function} pairs. functions must be async.
                         return True to exit
    :param timeout     : time in seconds for how long the buttons work for.
    :param only_author : only allow the user who used the command use the buttons
    :param single_use  : delete buttons after one is used
    """
    try:
        for emojiname in functions:
            await message.add_reaction(emojiname)
    except discord.errors.Forbidden:
        return

    def check(payload):
        return (
            payload.message_id == message.id
            and str(payload.emoji) in functions
            and not payload.member == ctx.bot.user
            and (
                (payload.member.id == ctx.bot.owner_id)
                if only_owner
                else (payload.member == ctx.author or not only_author)
            )
        )

    while True:
        try:
            payload = await ctx.bot.wait_for("raw_reaction_add", timeout=timeout, check=check)

        except asyncio.TimeoutError:
            break
        else:
            try:
                exits = await functions[str(payload.emoji)]()
            except discord.errors.NotFound:
                # message was deleted
                return
            try:
                await message.remove_reaction(payload.emoji, payload.member)
            except discord.errors.NotFound:
                pass
            except discord.errors.Forbidden:
                await ctx.send(
                    "`error: I'm missing required discord permission [ manage messages ]`"
                )
            if single_use or exits is True:
                break

    for emojiname in functions:
        try:
            await message.clear_reactions()
        except (discord.errors.NotFound, discord.errors.Forbidden):
            pass

class TwoWayIterator:
    """Two way iterator class that is used as the backend for paging."""

    def __init__(self, list_of_stuff):
        self.items = list_of_stuff
        self.index = 0

    def next(self):
        if self.index == len(self.items) - 1:
            return None
        self.index += 1
        return self.items[self.index]

    def previous(self):
        if self.index == 0:
            return None
        self.index -= 1
        return self.items[self.index]

    def current(self):
        return self.items[self.index]

async def paginate_list(ctx, items, use_locking=False, only_author=False, index_entries=True):
    pages = TwoWayIterator(items)
    if index_entries:
        msg = await ctx.send(f"`{pages.index + 1}.` {pages.current()}")
    else:
        msg = await ctx.send(pages.current())

    async def next_result():
        new_content = pages.next()
        if new_content is None:
            return
        if index_entries:
            await msg.edit(content=f"`{pages.index + 1}.` {new_content}", embed=None)
        else:
            await msg.edit(content=new_content, embed=None)

    async def previous_result():
        new_content = pages.previous()
        if new_content is None:
            return
        await msg.edit(content=new_content, embed=None)

    async def done():
        await msg.edit(content=f"{pages.current()}")
        return True

    functions = {"⬅": previous_result, "➡": next_result}
    if use_locking:
        functions["❌"] = done

    asyncio.ensure_future(reaction_buttons(ctx, msg, functions, only_author=only_author))



#Commands
@client.command(aliases=["ANIME", "a"])
@commands.cooldown(1,4,commands.BucketType.user)
async def anime(ctx, *, title):
    embed = animeSearch(title)
    await ctx.reply(embed=embed)
@client.command(aliases=["MANGA", "m"])
@commands.cooldown(1,4,commands.BucketType.user)
async def manga(ctx, *, title):
    embed = mangaSearch(title)
    await ctx.reply(embed=embed)
@client.command(aliases=["CHARACTER", 'ch', 'char'])
@commands.cooldown(1,4,commands.BucketType.user)
async def character(ctx, *, charName):
    embed = charSearch(charName)
    await ctx.reply(embed=embed)

@client.command(pass_context=True,help="Sends NSFW Pics.")
@commands.cooldown(1,4,commands.BucketType.user)
async def hentai(ctx):
  channels=[854454799705571389,854584851583991808,846428215953457162,852523342112096266]
  if ctx.channel.id not in channels:
    await ctx.reply("Command can only be used in Anime Channel or the Secret Cave lad")
    return  #async with ctx.channel.typing():
  try:
    async with aiohttp.ClientSession() as cs:
      async with cs.get('https://www.reddit.com/r/hentai/new.json?sort=hot%27') as a:
        res = await a.json()
        url = res['data']['children'] [random.randint(0, 25)]['data']['url']
        await ctx.reply(url)
  except aiohttp.ClientError:
    await ctx.reply("Try again")

@client.command(aliases=["yt"])
async def youtube(ctx, *, query):
    """Search videos from youtube."""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key":"AIzaSyBMlyaOzxE31TGgUVlq8p2Bm_PeLZ1qeFo",
        "part": "snippet",
        "type": "video",
        "maxResults": 25,
        "q": query,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 403:
                raise exceptions.Error("Daily youtube api quota reached.")

            data = await response.json()

    if not data.get("items"):
        return await ctx.send("No results found!")

    await paginate_list(
        ctx,
        [f"https://youtube.com/watch?v={item['id']['videoId']}" for item in data.get("items")],
        use_locking=True,
        only_author=True,
        index_entries=True,
    )

client.run('ODY4Mzk3Mzk1NzAzMTI0MDE4.YPvEGQ.KzjraqAVZHTxW5p1ggJW7cc2qkk')
