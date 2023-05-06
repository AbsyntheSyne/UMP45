import os.path

from disnake import Intents
from disnake.ext.commands import InteractionBot, CommandSyncFlags
import yaml
import pickle

from CommandCog import CommandCog
from ListenerCog import ListenerCog

ints = Intents.all()
cmdFlags = CommandSyncFlags.all()
client = InteractionBot(command_sync_flags=cmdFlags, intents=ints, test_guilds=[771800937794109440])

if not os.path.isfile("elems.sav"):
    with open("elems.sav", "wb") as file:
        pickle.dump([False, None, []], file)
    client.logChannel = None
    client.logChannelID = None
    client.doLog = False
    client.ignoredChannels = []
else:
    with open("elems.sav", "rb") as file:
        data = pickle.load(file)
    client.logChannelID = data[1]
    client.logChannel = None
    client.doLog = data[0]
    client.ignoredChannels = data[2]

client.add_cog(ListenerCog(client))
client.add_cog(CommandCog(client))

@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')
    if client.logChannelID is not None:
        client.logChannel = await client.fetch_channel(client.logChannelID)


with open('bot.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


if __name__ == "__main__":
    client.run(data['token'])