import discord, logging, requests, json, csv, re, aiohttp, io, os
from dotenv import dotenv_values
from discord.ext import commands
description = '''Bot description here'''
bot = commands.Bot(command_prefix='!geckobot', description=description, intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())
CHANNEL_TO_COMM_IN = 1094093145806999612
config = dotenv_values(".env")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # channel = client.get_channel(1056118223633928328)
    # await channel.send('hello')

@client.event
async def on_message(message): 
    if message.author == client.user:
        return
    if message.author.id != 382757219621666816:
        return
    # if '{}'.format(message.channel.id) != '{}'.format(CHANNEL_TO_COMM_IN):
    #     return
    if message.content.startswith('$yowallet'):
        splitMessage = message.content.split()
        send = splitMessage[1]
        if send == 'send':
            tokenAmt = splitMessage[2]
            tokenSymbol = splitMessage[3]
            recepient = splitMessage[5]
            print('{}\n{}\n{}'.format(tokenAmt,tokenSymbol,recepient))
            txObj = {'symbol': '{}'.format(tokenSymbol), 'recepient': '{}'.format(recepient), 'amount': '{}'.format(tokenAmt)}
            await message.channel.send('Sending Token, standby...')
            tokenSend = requests.post('http://127.0.0.1:42069/send-token', json = txObj)
            print(tokenSend.status_code)
            if tokenSend.status_code == 200:
                print('Res: {}'.format(tokenSend))
                await message.channel.send('Successfully sent {} {} to {}'.format(tokenAmt,tokenSymbol,recepient))
        else:
            print('We have logged in as {0.user}'.format(client))

        
        print('Res: {}'.format(tokenSend))
client.run(config['APP_TOKEN'])