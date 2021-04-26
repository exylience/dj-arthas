import discord
import asyncio
import random
import youtube_dl
import os

from discord.ext import commands
from config import settings

from player import get_answer

bot = commands.Bot(command_prefix=settings['prefix'])


@bot.event
async def on_ready():
    print('Bot online.')


@bot.command(pass_context=True)
async def hello(ctx):
    print(ctx.message)
    author = ctx.message.author

    await ctx.send(f'Fuck you, {author.mention}!')


@bot.command(pass_context=True)
async def p(ctx, url: str):
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name='Основной')
    await voice_channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    #voice.play(discord.FFmpegPCMAudio("assets/sounds/welcome.mp3"))

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music/%(extractor_key)s/%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
            {'key': 'FFmpegMetadata'},
        ],
        'reactrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': True,
        'quiet': False,
        'no_warnings': False,
        'default_search': 'auto',
        'source_addreacs': '0.0.0.0',  # bind to ipv4 since ipv6 addreacses cause issues sometimes
        'output': r'youtube-dl'
    }

    ffmpeg_options = {
        'before_options': '-nostdin',
        'options': '-vn'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        info_dict = ydl.extract_info(url, download=False)
        file_name = ydl.prepare_filename(info_dict)
        await ctx.send(f'Включаю трек {info_dict["title"]} :musical_note:')

        print(file_name)

        ydl.download([url])

        file_name = file_name.split('\\')
        print(file_name)
        file_name = file_name[2]
        file_name = file_name.replace('.webm', '.mp3')

    voice.play(discord.FFmpegPCMAudio(
        f"music/Youtube/{file_name}",
        options=ffmpeg_options),
        after=lambda x: os.remove(f"music/Youtube/{file_name}")
    )

    # https://www.youtube.com/watch?v=HrAclaz5GvA


@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("И откуда мне отключаться?")


@bot.command()
async def search(ctx):
    await ctx.send('Searching...')

    answer = get_answer()
    print(answer)


@bot.command(pass_context=True)
async def flip(ctx):
    await ctx.send('Монета подбрасывается...')
    rand = random.randint(1, 2)

    if rand == 1:
        await ctx.send(':full_moon: Орёл!')
    else:
        await ctx.send(':new_moon: Решка!')


bot.run(settings['token'])
