import random

import discord
import asyncio
import json
import sys

import dbhandler
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
        print(message.content)
        if message.content.startswith('!cp'):
            arguments = message.content.split()
            '''
            await client.send_message(message.channel,
            'The bot reads your command and sees {} arguments.'.format(len(arguments)))
            '''
            if len(arguments) == 1:
                if arguments[0] == '!cp' or arguments[0] == '!cphelp':
                    await client.send_message(message.channel, config['helptext'].format(config['version']))

            if len(arguments) == 2:
                if arguments[1] == 'give':
                    if message.author.id == config['noodles'] and message.channel.id == config['channelid']:
                        pass
                    else:
                        await client.send_message(message.channel,'You need to be Chop to do this.')
                    # TODO: Verify if user is valid.

                if arguments[1] == 'balance':
                    pass
                    # TODO: SQL Select and print here

                if arguments[1] == 'take':
                    if message.author.id == config['noodles'] and message.channel.id == config['channelid']:
                        pass
                    else:
                        await client.send_message(message.channel, 'You need to be Chop to do this.')
                    #TODO: Same as give but negative

            if len(arguments) > 4:
                await client.send_message(message.channel,
                                          "Too many arguments! Please see `!cp help` for valid command and usage.")

        if message.content.startswith('!cmtest'):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1

            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
            print(message.channel)
        elif message.content.startswith('!sleep'):
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Done sleeping')


async def statuschanger():
    statusindex = random.randint(0, len(config['status']))
    await client.change_status(game=discord.Game(name=config['status'][statusindex]))
    print('Status chnaged.')
    await asyncio.sleep(60*30) #asyncio is in seconds, so we doing it every 30 min



with open('bot.conf') as data_file:
    config = json.load(data_file)

check = dbhandler.connect()
if not check:
    sys.exit(1)
check = dbhandler.create()
if not check:
    sys.exit(1)

client.run(config['token'])
client.loop.create_task(statuschanger())