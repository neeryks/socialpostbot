import discord
from savedfile import discord_api
from quotegetter import Quote_Getter

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        print('Message from', message.author, ':', message.content)
        data = Quote_Getter(message.content).answer_back()
        return await message.channel.send(data)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_api())