# renbot

Simple self-hosted TTS Discord bot using UnrealSpeech's text-to-speech API. Can have up to 4 users talking simultaneously.

## Setup
- Create a new Discord bot on https://discord.com/developers/applications.
- From the "Bot" page, get the token (hit "reset token" if needed) and copy/paste that into the `sample.env` file where it says `BOT_TOKEN_HERE`.
- Also from the "Bot" page, make sure the Privileged Gateway Intents - Presence, Server Members, and Message Content - are ENABLED.
- Install Python if you haven't already.
- (Recommended but *technically* optional) Create a Python virtual environment for the bot.
- Run `pip install unrealspeech`.
- Go to https://unrealspeech.com/ and make an account.
- Once you've signed in, from the dashboard, copy your API key.
- Paste your API key into the `sample.env` file where it says `API_KEY_HERE`.
- Rename `sample.env` to simply `.env`.
- Run `python -m main.py` to start the bot.

## Using the bot

### Getting Started
- Type in `rb!start` to open a session associated with your account. (A "session" is *NOT* a voice channel connection.) This will create a user session with the bot with a default voice, speed, pitch, and expressiveness.
- Type `rb!settings` while you have a session open to view your current settings.
- Use `rb!connect` *WHILE YOU ARE IN A VOICE CHANNEL **AND** WHILE YOU HAVE A SESSION OPEN* to get the bot to connect to the voice channel.
- The bot will now read out anything *you specifically* type into the *voice chat associated with the voice channel you are in.* It will not read out messages anywhere else.
- To delete all your settings, be sure your session is open, then type `rb!delete`.
- If you want to close your session but *NOT* delete settings, type in `rb!close`.
- To disconnect the bot from a voice channel, type in `rb!disconnect`.

### Changing Settings

- Use `rb!voice [voicename]` to change the voice. Available voices are Liv, Scarlett, Amy, Dan, and Will.
- Use `rb!pitch [pitch value]` to change pitch. Pitch value must be a number between 0.5 and 1.5.
- Use `rb!speed [speed value]` to change speed. Speed value must be a number between 0 and 1.
- Use `rb!express [expressiveness value]` to change expressiveness. Expressiveness value must be a number between 0 and 1. (Lower is less expressive, higher is more expressive.)
- Use `rb!sayname [true/false]` to change whether the bot says your username along with your message (defaults to false).

## All commands

- `rb!help` - help info
- `rb!start` - start a session
- `rb!settings` - view current session settings
- `rb!connect` - connect to a voice channel
- `rb!disconnect` - disconnect from a voice channel
- `rb!voice` - change user voice
- `rb!speed` - change spoken speed
- `rb!pitch` - change spoken pitch
- `rb!express` - change spoken expressiveness
- `rb!sayname` - change whether bot says username
- `rb!close` - close session
- `rb!delete` - delete settings