import discord, logging, requests, json, csv, re, aiohttp, io, os
from dotenv import dotenv_values
from discord.ext import commands
description = '''Bot description here'''
bot = commands.Bot(command_prefix='!geckobot', description=description, intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())
CHANNEL_TO_COMM_IN = 1094093145806999612
geckometadatajsonfile = open('./geckos-metadata.json')
geckometadata = json.load(geckometadatajsonfile)
geckometadatajsonfile.close()
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
    if message.author.id != '382757219621666816':
        return
    if '{}'.format(message.channel.id) != '{}'.format(CHANNEL_TO_COMM_IN):
        return
    if message.content.startswith('$getcred'):
        await message.channel.send('Checking CRED balance, standby...')
        arggecknum = message.content.split()[1]
        arggecknum = re.sub('[^A-Za-z0-9]+', '', arggecknum)
        geckostats = requests.get('https://galacticgeckos-ni5j6e99z-ggsg-team.vercel.app/api/stats').json()
        tokenAddress = geckometadata[arggecknum]['TokenAddress']
        found = False
        for journeyinfo in geckostats['stakeEntryListReadable']:
                if journeyinfo['originalMint'] == tokenAddress:
                    print('FOUND! {}'.format(tokenAddress))
                    found = True
                    credBalance = journeyinfo['totalPoints'] /100
                    credMessage = '```CRED Balance: {}```'.format(credBalance)
                    await message.channel.send(credMessage)
                    break
        
        if not found:
            await message.channel.send('We\'re Sorry. Geck {} has no CRED :('.format(arggecknum))
        # await message.channel.send(geckostats[1])
    if message.content.startswith('$geckinfo'):
        await message.channel.send('Looking up Gecko, standby...')
        arggecknum = message.content.split()[1]
        arggecknum = re.sub('[^A-Za-z0-9]+', '', arggecknum)
        geckostats = requests.get('https://galacticgeckos-ni5j6e99z-ggsg-team.vercel.app/api/stats').json()
        gecko = geckometadata[arggecknum]
        tokenAddress = gecko['TokenAddress']
        found = False
        for journeyinfo in geckostats['stakeEntryListReadable']:
                if journeyinfo['originalMint'] == tokenAddress:
                    print('FOUND! {}'.format(tokenAddress))
                    heliusurl = "https://api.helius.xyz/v1/nft-events?api-key={}".format(config['HELIUS_TOKEN'])
                    found = True
                    credBalance = journeyinfo['totalPoints'] /100
                    if journeyinfo['amount'] != 1:
                        journeyduration = "Not on Journey, SEND IT!"
                    else:
                        journeyduration = journeyinfo['lockPeriodNum']
                    geckoMessage = '```Name: Galactic Gecko #{} \nCRED Balance: {}\nToken Address: {}\nJourney Duration: {}```'.format(gecko['Number'], credBalance, tokenAddress, journeyduration)
                    async with aiohttp.ClientSession() as session: # creates session
                        async with session.get(gecko['Image']) as resp: # gets image from url
                            img = await resp.read() # reads image from response
                            with io.BytesIO(img) as file: # converts to file-like object
                                await message.channel.send(file=discord.File(file, 'gecko.png'))
                    await message.channel.send(geckoMessage)
                    break
        if not found:
            geckoMessage = '```Name: Galactic Gecko #{} \nCRED Balance: {}\nToken Address: {}\nJourney Duration: {}```'.format(gecko['Number'], "0", tokenAddress, "0")
            async with aiohttp.ClientSession() as session: # creates session
                async with session.get(gecko['Image']) as resp: # gets image from url
                    img = await resp.read() # reads image from response
                    with io.BytesIO(img) as file: # converts to file-like object
                        await message.channel.send(file=discord.File(file, 'gecko.png'))
            await message.channel.send(geckoMessage)
    if message.content.startswith('$geckobot'):
        arg = message.content.split()[1]
        if '{}'.format(arg) == 'help':
            helpmessage = '```Available Commands: \n$getcred <geckonumber> : Get CRED balance for provided Gecko number\n$geckinfo <geckonumber> : Detailed info regarding a Gecko```'
            await message.channel.send(helpmessage)

client.run(config['APP_TOKEN'])