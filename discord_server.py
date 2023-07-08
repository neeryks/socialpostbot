
import discord
from helper_functions.querysorter import Quote_Getter
from discordapi import discord_api

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
        await message.attachments[0].save("static_media/video_demo.mp4")
        data = Quote_Getter(message.content).answer_back()
    if data == "quote.mp3":
        await message.channel.send(file=discord.File('saved_media/quote.mp3'))
    if data == "image.png":
        await message.channel.send(file=discord.File('saved_media/image.png'))
    if data == "final_video.mp4":
        await message.channel.send(file=discord.File('saved_media/final_video.mp4'))
    else:
        data = Quote_Getter(message.content).answer_back()
        try:
            await message.channel.send(data)
        except:
            await message.channel.send("Unknown Error Occured , Please Try Again")

if __name__ == "__main__":

    client.run(discord_api())
