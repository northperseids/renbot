import discord
import os
import dotenv
import asyncio
from unrealspeech import UnrealSpeechAPI, play, save
import io

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
prefix = 'rb!'

# ---------- EDIT UNDER HERE

# Get your API key from unrealspeech.com - follow github instructions.
api_key = 'b9NSkg3mzfveRHrGu9ivwRwWzLmhrOsYATTIOMusRnJoZkNH8gRMZF'

# Don't change this unless you really know what you're doing!
BITRATE = "192k"

# ---------- DO NOT EDIT PAST HERE

speech_api = UnrealSpeechAPI(api_key)

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

users = []

class User():
    def __init__(self, voicechannel, userid, voicename='Liv', speed=0, pitch=1.0, temperature=0.70):
        self.voicechannel = voicechannel
        self.id = userid
        self.voicename = voicename
        self.speed = speed
        self.pitch = pitch
        self.temperature = temperature

@client.event
async def on_ready():
    print(f'{client.user} is online!')

@client.event
async def on_message(message):

    # make all messages lowercase
    msg = message.content.lower()

    if msg.startswith(prefix + 'start'):
        if len(users) >= 4:
            await message.channel.send('Too many users! Session not started.')
            return
        try:
            user = User(message.author.voice.channel.id, message.author.id)
            users.append(user)
            await message.channel.send(f'Session opened for {message.author.name}.')
            return
        except:
            await message.channel.send('Failed to open session! (If you are not in a voice channel, join one first.)')
            return
        
    if msg.startswith(prefix + 'help'):
        await message.channel.send(f'Hello!\n\nUp to 4 users can use this bot at once.\n\nTo get started, type in `{prefix}start`. This will open a session for you with a default voice, speed, pitch, and expression. Once you get the bot to join your voice channel, the bot will read out anything you type in the VOICE CHANNEL CHAT.\n\nTo change the voice, speed, pitch, or expressiveness, use the commands:\n- {prefix}voice [voice]\n- {prefix}speed [speed]\n- {prefix}pitch [pitch]\n- {prefix}express [expressiveness]\n\nThe possible voices are Liv, Scarlett, Amy, Will, and Dan. For speed and expressiveness, enter a number between 0 and 1. For pitch, a number between 0.5 and 1.5.\n\nTo get the bot to join a voice channel, type in `{prefix}connect`. You will need to both have an open session *AND* be in a voice channel yourself in order for the bot to know where to join. To disconnect, type in `{prefix}disconnect`.')
        return

    if msg.startswith(prefix + 'settings'):
        for user in users:
            if user.id == message.author.id:
                await message.channel.send(f'User session for {message.author.name}:\n\n**Voice:** {user.voicename}\n**Speed:** {user.speed}\n**Pitch:** {user.pitch}\n**Expressiveness:** {user.temperature}')
                return
        await message.channel.send('No open session found.')
        return

    if msg.startswith(prefix + 'voice '):
        mes = message.content[9:]
        if mes == 'Liv' or mes == 'Scarlett' or mes == 'Amy' or mes == 'Dan' or mes == 'Will':
            pass
        else:
            await message.channel.send('Invalid voice name!')
            return
        for user in users:
            if user.id == message.author.id:
                user.voicename = mes
                await message.channel.send(f'Voice changed to {mes}.')
                return
        await message.channel.send('No open session found.')
        return

    if msg.startswith(prefix + 'pitch '):
        mes = message.content[9:]
        if 0.5 <= mes <= 1.5:
            pass
        else:
            await message.channel.send('Invalid pitch value! Enter a number between 0.5 and 1.5.')
            return
        for user in users:
            if user.id == message.author.id:
                user.pitch = mes
                await message.channel.send(f'Pitch changed to {mes}.')
                return
        await message.channel.send('No open session found.')
        return

    if msg.startswith(prefix + 'express '):
        mes = message.content[11:]
        if 0 <= mes <= 1:
            pass
        else:
            await message.channel.send('Invalid expression value! Enter a number between 0 and 1.')
            return
        for user in users:
            if user.id == message.author.id:
                user.pitch = mes
                await message.channel.send(f'Expression variation changed to {mes}.')
                return
        await message.channel.send('No open session found.')
        return

    if msg.startswith(prefix + 'speed '):
        mes = message.content[9:]
        if 0 <= mes <= 1:
            pass
        else:
            await message.channel.send('Invalid speed value! Enter a number between 0 and 1.')
            return
        for user in users:
            if user.userid == message.author.id:
                user.pitch = mes
                await message.channel.send(f'Speed changed to {mes}.')
                return
        await message.channel.send('No open session found.')
        return

    if msg.startswith(prefix + 'close'):
        try:
            my_filter = filter(lambda x: x[1].id == message.author.id, enumerate(users))
            index = next(my_filter)[0]
            del users[index]
            await message.channel.send(f'Session for {message.author.name} closed.')
            return
        except:
            await message.channel.send('Error! (Did you have an open session?)')
        return

    for user in users:
        if user.id == message.author.id and message.channel.id == user.voicechannel:

            if msg.startswith(prefix + 'connect'):
                try:
                    await message.author.voice.channel.connect()
                except:
                    await message.channel.send('Error! (You are probably either in a channel already, or are not in one at all!)')

            elif msg.startswith(prefix + 'disconnect'):
                try:
                    vc = discord.utils.get(client.voice_clients, guild=message.guild)
                    await vc.disconnect()
                except:
                    await message.channel.send('Error! (If you cannot disconnect the bot through commands, right-click on it and select Disconnect.)')

            else:
                voice_channel = discord.utils.get(client.voice_clients, guild=message.guild)
                if voice_channel is None:
                    return

                # Generate audio from text
                audio_data = speech_api.stream(
                    text=msg, voice_id=user.voicename, bitrate=BITRATE, speed=user.speed, pitch=user.pitch, temperature=user.temperature
                )

                stream = io.BytesIO(audio_data)

                vc = discord.utils.get(client.voice_clients, guild=message.guild)
                vc.play(discord.FFmpegPCMAudio(stream, pipe=True))
                while vc.is_playing():
                    await asyncio.sleep(.1)
            return
        
    if msg.startswith(prefix):
        await message.channel.send(f'No open sessions or no open voice channel. See `{prefix}help` for more info.')
        return

client.run(token)