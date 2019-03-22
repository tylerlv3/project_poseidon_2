import discord
from discord.ext import commands
import random
import asyncio
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import youtube_dl
import time



TOKEN = 'NTU1NTQ5ODQ3ODgxNzc3MTUz.D2tHxA.DY7FV9ULgEQoH2oUpsxQ69Q7wbY'

extensions = ['rndfacts']

client = commands.Bot(command_prefix='.')
client.remove_command('help')
client.remove_command('play')
#web scraping
    # Events

@client.event
async def on_member_join(member):
    join_msg = 'Welcome to the server, we hope you enjoy! To use any commands please use the prefix "." before the command desired. For help type ".help"'
    await client.send_message(member, join_msg)
    join_serv_message = ' Just joined, Welcome!'
    await client.send_message(discord.Object(id='555893854952226837'), member.mention + join_serv_message)
    print('A user has joined the server')

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="In the Best Server Ever!"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extensions(extension)
        except Exception as error:
            print('{} Cannot load [{}]'.format(extension, error))



    # Commands
@client.command(pass_context = True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    if amount < 2:
        await client.say('You must delete atlesast 2 messages!')
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages Deleted.')
    print('A member has used a command')

@client.command()
async def help():
    await client.say('For Help Please DM <@&555587892349632514>, for commands please use ".commands"')
    print('A member has used a command')

@client.command()
async def flip():
    flip_list = ["Heads", "Tails"]
    flipped = random.choice(flip_list)
    await client.say('You got: ' + flipped)
    print('A member has used a command')

@client.command(pass_context=True)
async def commands(ctx):
    author = ctx.message.author
    cmd_list = '" .help "     - Gives instructions for what to do if you need help\n" .commands "       - Shows a list of availble commands and what their function is\n" .clear "      - Used to clear the previous messages, enter a number after command for a specific amount you want deleted\n" .flip "     - Chooses heads or tails at random\n" .bitcoin "      - Shows the price of bitcoin at the time the command is used'
    await client.send_message(author, cmd_list)
    print('A member has used a command')

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(8)
        players[id] = player
        player.start()

@client.command(pass_context=True)
async def join(ctx):
    channel_voice = ctx.message.author.voice.voice_channel
    try:
        await client.join_voice_channel(channel_voice)
    except:
        await client.say("You Must Be In a Channel for me to Join. (Try Again Once in a Channel)")


@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    try:
        await voice_client.disconnect()
    except:
        await client.say("I must be in a Voice channel to leave.")
    print("A member has used a command")


@client.command(pass_context=True)
async def play(ctx):
    if "www.youtube.com" not in ctx.message.content:
        await client.say("Your request must have a YouTube URL in it.")
    else:
        try:
            channel_voice = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel_voice)
            try:
                yt_url = ctx.message.content
                link = yt_url.replace('.play ', '')
                await client.say("Playing :white_check_mark:")
                url = link.strip()
                print(url)
                print('test')
                server = ctx.message.server
                voice_client = client.voice_client_in(server)
                player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
                players[server.id] = player
                player.start()
            except:
                await client.say("Must be a YouTube URL")
        except:
            await client.send_message(ctx.message.channel, "You Must Be In a Channel for me to Join. (Try Again Once in a Channel)")


@client.command(pass_context=True)
async def pause(ctx):
    try:
        id = ctx.message.server.id
        players[id].pause()
        print("A member has paused audio")
        await client.say("Paused")
    except:
        await client.say("There Must be audio playing for me to pause.")

@client.command(pass_context=True)
async def stop(ctx):
    try:
        id = ctx.message.server.id
        players[id].stop()
        print("A member has stopped audio")
    except:
        await client.say("There Must be audio playing for me to stop.")

@client.command(pass_context=True)
async def resume(ctx):
    try:
        id = ctx.message.server.id
        players[id].resume()
        print("A member has resumed audio")
    except:
        await client.say("There Must be audio paused for me to resume.")

@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say("Audio Queued.")

@client.command(pass_context=True)
async def bitcoin(ctx):
    author = ctx.message.author
    site = 'https://cointelegraph.com/bitcoin-price-index'
    uClient = uReq(site)
    pg_html = uClient.read()
    uClient.close()
    page_souped = soup(pg_html, "html.parser")
    bc_price = page_souped.find("div", {"class": "price-value"})
    bc_volatility = page_souped.find("div", {"class": "day-percent"})
    bc_price_text = bc_price.get_text()
    bc_volatility_text = bc_volatility.get_text()
    await client.say('The current price of Bitcoin is: ' + bc_price_text)
    await client.say("Change From Yesterday: " + bc_volatility_text)
    print('A member has used a command')


@client.command(pass_context=True)
async def ethereum(ctx):
    author = ctx.message.author
    site = 'https://cointelegraph.com/ethereum-price-index'
    uClient = uReq(site)
    pg_html = uClient.read()
    uClient.close()
    page_souped = soup(pg_html, "html.parser")
    et_price = page_souped.find("div", {"class": "price-value"})
    et_vol = page_souped.find("div", {"class": "day-percent"})
    et_vol_text = et_vol.get_text()
    et_price_text = et_price.get_text()
    await client.say('The current price of Ethereum is: ' + et_price_text)
    await client.say("Change From Yesterday: " + et_vol_text)
    print('A member has used a command')



client.run(TOKEN)

#@client.command()
#async def CommandName()

    #print('A member has used a command')
