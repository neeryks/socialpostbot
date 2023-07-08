
import discord
from quotegetter import Quote_Getter
from savedfile import discord_api as discord_key

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    data = Quote_Getter(message.content).answer_back()
    if message.attachments != []:
        data = Quote_Getter(message.content).answer_back()
        await message.attachments[0].save("video_demo.mp4")
        data = Quote_Getter(message.content).answer_back()
    if data == "quote.mp3":
        await message.channel.send(file=discord.File('quote.mp3'))
    if data == "image.png":
        await message.channel.send(file=discord.File('image.png'))
    if data == "final_video.mp4":
        await message.channel.send(file=discord.File('final_video.mp4'))
    else:
        data = Quote_Getter(message.content).answer_back()
        try:
            await message.channel.send(data)
        except:
            await message.channel.send("Unknown Error Occured , Please Try Again")

client.run(discord_key())
