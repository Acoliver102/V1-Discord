import os

import discord
from discord.ext import commands
import random
import subprocess as sp
import time
from pathlib import Path

description = '''Funny ULTRAKILL voice.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def join(ctx):
    print(ctx.author.voice.channel.id)
    await ctx.author.voice.channel.connect()


@bot.command()
async def v1(ctx, *, message):
    # generate audio file with funny voice - overwrite existing file
    process = sp.Popen('sam.exe -wav temp.wav ' + message + ' .', shell=True,
                       cwd=r'YOUR WORKING DIRECTORY HERE')

    # open file buffer
    with open('temp.wav', 'rb') as tmp_buf:

        # play from source
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("temp.wav", pipe=False))

        # check if in VC, if not: join VC of caller
        current_vc = ctx.voice_client
        if ctx.author.voice is not None:
            if current_vc is None:
                await ctx.author.voice.channel.connect()
            elif current_vc.channel.id == ctx.author.voice.channel.id:
                pass
            else:
                await current_vc.move_to(ctx.author.voice.channel)

            # play audio
            print('Attempting play!')
            ctx.voice_client.play(source)
        else:
            # can't play without a source / VC
            await ctx.send("```ERROR: NO VOCAL INTERFACE DETECTED. UNABLE TO COMPLETE TASK```")



@bot.command()
async def disconnect(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()


bot.run('Bot token here')
