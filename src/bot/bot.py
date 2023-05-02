import discord, logging, requests, json, csv, re, aiohttp, io, os, base58
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

def isProbablyWalletAddress(solanaAddress):
    if not isinstance(solanaAddress, str):
        return False

    # Check that the address is 32 bytes long
    if len(solanaAddress) != 44:
        return False

    # Check that the address contains only hexadecimal characters
    try:
        bytes.fromhex(solanaAddress[3:])
    except ValueError:
        return False

    return True

async def handleRequest(type, url, data = {}):
    try:
        if type == 'get':
            return await requests.get(url)
        elif type == 'post':
            return await requests.post(url, json = data)
        elif type == 'delete':
            return await requests.delete(url, json = data)
        elif type == 'put':
            return await requests.put(url, json = data)
    except:
        return {'success': 'false', 'message': 'A {} request exception occured! url: {}'.format(type,url)}

async def sendTxn(tokenSymbol, recepient, tokenAmt):
    txObj = {'symbol': '{}'.format(tokenSymbol), 'recepient': '{}'.format(recepient), 'amount': '{}'.format(tokenAmt)}
    tokenSend = await handleRequest('post', 'http://127.0.0.1:42069/send-token-to-address', json = txObj)
    return tokenSend

async def queueReactionCampaign(tokenSymbol, tokenAmt, reactionLimit):
    txObj = {'symbol': '{}'.format(tokenSymbol), 'amount': '{}'.format(tokenAmt), 'reactionLimit': '{}'.format(reactionLimit)}
    queueCampaign = await handleRequest('post', 'http://127.0.0.1:42069/init-reaction-campaign', json = txObj)
    return queueCampaign

async def getWalletDiscordUser(discordUser):
    userWallet = await handleRequest('get', 'http://127.0.0.1:42069/get-wallet-by-discord-user?discord_user={}'.format(discordUser))
    return userWallet

async def getActiveCampaign(messageId):
    campaign = await handleRequest('get', 'http://127.0.0.1:42069/get-active-reaction-campaigns?message_id={}'.format(messageId))
    return campaign

@client.event
async def on_reaction_add(reaction, user):
    print('message_id: {}'.format(reaction.message.id))
    activeCampaign = getActiveCampaign(reaction.message.id)
    if(activeCampaign != [] and activeCampaign['totalReactions'] <= activeCampaign['maxReaction']):
        wallet = getWalletDiscordUser(user)
        return sendTxn(activeCampaign.tokenSymbol, wallet, activeCampaign.amtToSend)

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
        tokenAmt = splitMessage[2]
        tokenSymbol = splitMessage[3]
        fifthArg = splitMessage[5]

        if send == 'send':
            if fifthArg == 'the':
                if splitMessage[6] == 'first':
                    reactionLimit = splitMessage[7]
                    print('queue reaction based campaign')
                    queuedCampaign = queueReactionCampaign(tokenSymbol, tokenAmt, reactionLimit)
                    if queuedCampaign.json()["success"] == "true":
                        await message.channel.send('Successfully started campain for {} {} for the first {} reactions'.format(tokenAmt,tokenSymbol,recepient))
                    else:
                        await message.channel.send('Transaction failed')

            if isProbablyWalletAddress(fifthArg) == True:
                recepient = splitMessage[5]
                await message.channel.send('Sending Token, standby...')
                sendToken = sendTxn(tokenSymbol, recepient, tokenAmt)
                if sendToken.status_code == 200:
                    sendTokenJson = sendToken.json()
                    print('Res: {}'.format(sendTokenJson))
                    if sendToken.json()["success"] == "true":
                        await message.channel.send('Successfully sent {} {} to {} https://solscan.io/tx/{}?cluster=devnet'.format(tokenAmt,tokenSymbol,recepient,sendTokenJson["tx_signature"]))
                    else:
                        await message.channel.send('Transaction failed')
        else:
            print('Invalid command')
            await message.channel.send('Invalid Command')
client.run(config['APP_TOKEN'])