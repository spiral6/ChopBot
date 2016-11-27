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
    if message.content.startswith(prefix):
        arguments = message.content.split()
        '''
            await client.send_message(message.channel,
            'The bot reads your command and sees {} arguments.'.format(len(arguments)))
            '''
        if len(arguments) == 1:
            if arguments[0] == prefix or arguments[0] == prefix + 'help':
                await client.send_message(message.channel, helptext)

        elif len(arguments) <= 4:
            if arguments[1] == 'help':
                await client.send_message(message.channel, helptext)

            if arguments[1] == 'give' or arguments[1] == 'add':
                if message.author.id == config['master']:
                    # and message.channel.id == config['channelid'] for constraining to one channel.
                    userid = re.match(r'<@!?(?P<id>\d+)>', arguments[3])
                    if userid is None:
                        await client.send_message(message.channel,
                                                  'Error: Invalid usage of command.\n`{} give <amount> <user>`'.format(prefix))
                    else:
                        status = dbhandler.addbalance(int(userid.group('id')), arguments[2])
                        if status == 'sqlerrorfromcheckbalance':
                            print('Can\'t add to balance due to database error in checkbalance().')
                            await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')

                        elif status == 'addeduserandbalance':
                            print('Added user {} and balance {} successfully.'.format(userid.group('id'),
                                                                                      arguments[2]))
                            replymessage = '{} has gained {}'.format(arguments[3], arguments[2]) + currencyname + '.'
                            await client.send_message(message.channel, replymessage)

                        elif status == 'updatedbalance':
                            print('Updated balance for user {}'.format(userid.group('id')))
                            replymessage = '{} has gained {}'.format(arguments[3], arguments[2]) + currencyname + '.'
                            await client.send_message(message.channel, replymessage)

                        elif status == 'sqlerrorfromaddbalance':
                            print('Can\'t add to balance due to database error in addbalance().')
                            await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')

                        else:
                            print('I have no idea how you got here.')
                else:
                    member = message.server.get_member(config['master'])
                    await client.send_message(message.channel,
                                              'You need to be {} to do this.'.format(member.display_name))

            if arguments[1] == 'balance':
                status = dbhandler.checkbalance(message.author.id)
                if not status:
                    await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')
                else:
                    replymessage = 'You have {} '.format(status[0]) + currencyname + '.'
                    await client.send_message(message.channel, replymessage)
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
                        if counter >= 5:  # 5 person limit
                            pass
                        else:
                            print(s)
                            member = message.server.get_member(str(s[0]))
                            leaderboard += str(counter + 1) + ". " + member.display_name + " - " + str(
                                s[1]) + currencyname + "\n"
                        counter += 1
                    await client.send_message(message.channel, leaderboard)

            if arguments[1] == 'take' or arguments[1] == 'subtract':
                if message.author.id == config['master'] and message.channel.id == config['channelid']:
                    userid = re.match(r'<@(?P<id>\d+)>', arguments[3])
                    if userid is None:
                        await client.send_message(message.channel,
                                                  'Error: Specify a user.\n`{} give <amount> <user>`'.format(prefix))
                    else:
                        status = dbhandler.addbalance(int(userid.group('id')), float(arguments[2]) * -1)
                        if status == 'sqlerrorfromcheckbalance':
                            print('Can\'t add to balance due to database error in checkbalance().')
                            await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')
                        elif status == 'addeduserandbalance':
                            print('Added user {} and balance {} successfully.'.format(userid.group('id'),
                                                                                      arguments[2]))
                            replymessage = '{} has lost {} '.format(arguments[3], arguments[2]) + currencyname + '.'
                            await client.send_message(message.channel, replymessage)

                        elif status == 'updatedbalance':
                            print('Updated balance for user {}'.format(userid.group('id')))
                            replymessage = '{} has lost {} '.format(arguments[3], arguments[2]) + currencyname + '.'
                            await client.send_message(message.channel, replymessage)

                        elif status == 'sqlerrorfromaddbalance':
                            print('Can\'t add to balance due to database error in addbalance().')
                            await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')
                        else:
                            print('I have no idea how you got here.')
                else:
                    member = message.server.get_member(config['master'])
                    await client.send_message(message.channel,
                                              'You need to be {} to do this.'.format(member.display_name))

        if len(arguments) > 4:
            await client.send_message(message.channel,
                                      "Too many arguments! Please see `{} help` for valid command and usage.".format(prefix))
    elif message.content.startswith('linkme'):
        arguments = message.content.split()
        if len(arguments) == 4:
            if arguments[1] == 'save' or arguments[1] == 'add':
                status = dbhandler.addlinkme(arguments[2], arguments[3])
                if status == 'sqlerrorfromchecklinkme':
                    print('Can\'t add to balance due to database error in checklinkme().')
                    await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')

                elif status == 'addedlinkme':
                    replymessage = 'Added {}: {} successfully.'.format(arguments[2], arguments[3])
                    print(replymessage)
                    await client.send_message(message.channel, replymessage)

                elif status == 'updatedlinkme':
                    replymessage = 'Updated {} with {}'.format(arguments[2], arguments[3])
                    print(replymessage)
                    await client.send_message(message.channel, replymessage)

                elif status == 'sqlerrorfromaddlinkme':
                    print('Can\'t add to linkme due to database error in addlinkme().')
                    await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')
                pass
        if len(arguments) == 2:
            text = dbhandler.getlinkme(arguments[1])
            if not text:
                print('Can\'t find text.')
                await client.send_message(message.channel, 'Sorry, wasn\'t able to complete that.')
            await client.send_message(message.channel, text)

@client.event
async def statuschanger():
    statusindex = random.randint(0, len(config['status']) - 1)
    await client.change_status(game=discord.Game(name=config['status'][statusindex]))
    print('Status changed to' + "\" " + config['status'][statusindex] + "\"")
    await asyncio.sleep(60 * 5)  # asyncio is in seconds, so we doing it every 5 min


with open('bot.conf') as data_file:
    config = json.load(data_file)

helptext = '''Hey, this is ChopBot version v{0}, made by spiral6.
Source: https://github.com/spiral6/ChopBot
Available commands are `{1} help`, `{1} balance`, `{1} leaderboard`.'''.format(config['version'], config['prefix'])
currencyname = config['currencyname']
prefix = config['prefix']

check = dbhandler.connect()
if not check:
    sys.exit(1)
check = dbhandler.create()
if not check:
    sys.exit(1)
check = dbhandler.createlinkme()
if not check:
    sys.exit(1)

client.run(config['token'])
client.loop.create_task(statuschanger())
