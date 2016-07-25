import discord
import asyncio
import json

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.author.id == config['noodles'] and message.channel.id == config['channelid']:
        if message.content.startswith('!cp'):
            arguments = message.content.split()
            '''
            await client.send_message(message.channel,
            'The bot reads your command and sees {} arguments.'.format(len(arguments)))
            '''
            if len(arguments) == 1:
                await client.send_message(message.channel, config['helptext'].format(config['version']))

            if len(arguments) == 2:
                if arguments[1] == 'give':
                    pass
                    # TODO: SQL Select and Update here, as well as logic handling for non-existent records

                if arguments[1] == 'balance':
                    pass
                    # TODO: SQL Select and print here
                
            if len(arguments) > 3:
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


with open('bot.conf') as data_file:
    config = json.load(data_file)
client.run(config['token'])
