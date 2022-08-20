import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

ttsLang = "sv"

from gtts import gTTS
from pydub import AudioSegment

@client.command(name="lang")
async def lang(ctx, lang):
    await ctx.channel.send("försöker att byte språk till " + lang)
    ttsLang = lang
    print(ttsLang)

@client.command(name="join")
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("Du e ju inte ens i en röstkanal mongo")
    voiceChannel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voiceChannel.connect()
    else:
        await ctx.voice_client.move_to(voiceChannel)

@client.command(name="leave")
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command(name="say")
async def say(ctx, *args):

    ctx.voice_client.stop()
    sentence = " ".join(args)
    FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
    await ctx.channel.send("Laddar...")

    soundObj = gTTS(text=sentence, lang=ttsLang, slow=True)
    soundObj.save("sound.mp3")

    os.system("ffmpeg.exe -i sound.mp3 -y -af asetrate=24000*0.7,aresample=24000 output.mp3")
    os.system('ffmpeg.exe -i output.mp3 -y -filter:a "volume=2" newoutput.mp3')
    await ctx.channel.send("Nu säger jag " + sentence + " 🥺🥺🤠🤓🧐🧐")

    vc = ctx.voice_client
    vc.play(discord.FFmpegPCMAudio(executable="./ffmpeg.exe", source="./newoutput.mp3"))



TOKEN = "YOUR TOKEN"


client.run(TOKEN)
