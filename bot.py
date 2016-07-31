#!/usr/bin/python3

import random
import re
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
    global helptext
    print('[Message] - ' + message.content)
    if message.content.startswith('!cp'):
        arguments = message.content.split()
        '''
            await client.send_message(message.channel,
            'The bot reads your command and sees {} arguments.'.format(len(arguments)))
            '''
        if len(arguments) == 1:
            if arguments[0] == '!cp' or arguments[0] == '!cphelp':
                await client.send_message(message.channel, helptext)

        elif len(arguments) <= 4:
            if arguments[1] == 'help':
                await client.send_message(message.channel, helptext)

            if arguments[1] == 'give' or arguments[1] == 'add':
                if message.author.id == config['noodles']:
                    # and message.channel.id == config['channelid'] for constraining to one channel.
                    userid = re.match(r'<@!?(?P<id>\d+)>', arguments[3])
                    if userid is None:
                        await client.send_message(message.channel,
                                                  'Error: Invalid usage of command.\n`!cp give <amount> <user>`')
                    else:
                        status = dbhandler.addbalance(int(userid.group('id')), arguments[2])
                        if status == 'sqlerrorfromcheckbalance':
                            print('Can\'t add to balance due to database error in checkbalance().')
                            await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')
                        elif status == 'addeduserandbalance':
                            print('Added user {} and balance {} successfully.'.format(userid.group('id'),
                                                                                      arguments[2]))
                            await client.send_message(message.channel,
                                                      '{} has gained {} ChopPoints.'.format(arguments[3],
                                                                                            arguments[2]))
                        elif status == 'updatedbalance':
                            print('Updated balance for user {}'.format(userid.group('id')))
                            await client.send_message(message.channel,
                                                      '{} has gained {} ChopPoints.'.format(arguments[3],
                                                                                            arguments[2]))
                        elif status == 'sqlerrorfromaddbalance':
                            print('Can\'t add to balance due to database error in addbalance().')
                            await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')
                        else:
                            print('I have no idea how you got here.')
                else:
                    await client.send_message(message.channel, 'You need to be Chop to do this.')

            if arguments[1] == 'balance':
                status = dbhandler.checkbalance(message.author.id)
                if not status:
                    await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')
                else:
                    await client.send_message(message.channel, 'You have {} ChopPoints.'.format(status[0]))
            if arguments[1] == 'leaderboard':
                status = dbhandler.leaderboard()
                if not status:
                    await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')
                else:
                    leaderboard = ''
                    counter = 0
                    for s in status:
                            if s[1] <= 0:
                                pass
                            if counter >= 5: #5 person limit
                                pass
                            else:
                                print(s)
                                member = message.server.get_member(str(s[0]))
                                leaderboard += str(counter+1) + ". " + member.display_name + " - " + str(s[1]) + " ChopPoints\n"
                            counter+=1
                    await client.send_message(message.channel, leaderboard)

            if arguments[1] == 'take' or arguments[1] == 'subtract':
                if message.author.id == config['noodles'] and message.channel.id == config['channelid']:
                    userid = re.match(r'<@(?P<id>\d+)>', arguments[3])
                    if userid is None:
                        await client.send_message(message.channel,
                                                  'Error: Specify a user.\n`!cp give <amount> <user>`')
                    else:
                        status = dbhandler.addbalance(int(userid.group('id')), float(arguments[2]) * -1)
                        if status == 'sqlerrorfromcheckbalance':
                            print('Can\'t add to balance due to database error in checkbalance().')
                            await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')
                        elif status == 'addeduserandbalance':
                            print('Added user {} and balance {} successfully.'.format(userid.group('id'),
                                                                                      arguments[2]))
                            await client.send_message(message.channel,
                                                      '{} has lost {} ChopPoints.'.format(arguments[3],
                                                                                          arguments[2]))
                        elif status == 'updatedbalance':
                            print('Updated balance for user {}'.format(userid.group('id')))
                            await client.send_message(message.channel,
                                                      '{} has lost {} ChopPoints.'.format(arguments[3],
                                                                                          arguments[2]))
                        elif status == 'sqlerrorfromaddbalance':
                            print('Can\'t add to balance due to database error in addbalance().')
                            await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')
                        else:
                            print('I have no idea how you got here.')
                else:
                    await client.send_message(message.channel, 'You need to be Chop to do this.')

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
    await asyncio.sleep(60 * 30)  # asyncio is in seconds, so we doing it every 30 min


with open('bot.conf') as data_file:
    config = json.load(data_file)

helptext = '''Hey, this is ChopBot version v{}, made by spiral6.
Source: https://github.com/spiral6/ChopBot
Available commands are `!cp help`, `!cp balance`, `!cp leaderboard`.'''.format(config['version'])

check = dbhandler.connect()
if not check:
    sys.exit(1)
check = dbhandler.create()
if not check:
    sys.exit(1)

client.run(config['token'])
client.loop.create_task(statuschanger())
