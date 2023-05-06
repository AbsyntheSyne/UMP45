import pickle

import disnake
from disnake import Permissions, ApplicationCommandInteraction, Embed
from disnake.ext.commands import Cog, slash_command

perms = Permissions(8)


class CommandCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(default_member_permissions=perms)
    async def dolog(self, inter: ApplicationCommandInteraction):
        self.bot.doLog = not self.bot.doLog
        yesNoLog = "now" if self.bot.doLog else "no longer"
        channelName = ((" in the channel #" + self.bot.logChannel.name) if self.bot.logChannel else " as soon as you configure a channel using /logchannel")
        embed = Embed(description="The bot will " + yesNoLog + " log" + channelName)
        with open("elems.sav", "wb") as file:
            pickle.dump([self.bot.doLog, self.bot.logChannel.id if self.bot.logChannel else None, self.bot.ignoredChannels], file)
        await inter.response.send_message(embed=embed)

    @slash_command(default_member_permissions=perms)
    async def logchannel(self, inter: ApplicationCommandInteraction, channel: disnake.TextChannel = None):
        if channel is None:
            self.bot.logChannel = inter.channel
        else:
            self.bot.logChannel = channel
        embed = Embed(description="The logging channel has been set to #" + self.bot.logChannel.name)
        with open("elems.sav", "wb") as file:
            pickle.dump([self.bot.doLog, self.bot.logChannel.id if self.bot.logChannel else None, self.bot.ignoredChannels], file)
        await inter.response.send_message(embed=embed)

    @slash_command()
    async def currentconfig(self, inter: ApplicationCommandInteraction):
        embed = Embed(title="Current configuration")
        embed.add_field("Are logs enabled", "Yes" if self.bot.doLog else "No", inline=False)
        embed.add_field("Log channel", "None" if self.bot.logChannel is None else self.bot.logChannel.mention, inline=False)
        ignoredChannels = ""
        for channelID in self.bot.ignoredChannels:
            ignoredChannels += (await self.bot.fetch_channel(channelID)).mention + "\n"
        if ignoredChannels == "":
            ignoredChannels = "No ignored channels"
        embed.add_field("ignored channels", ignoredChannels, inline=False)
        await inter.response.send_message(embed=embed)

    @slash_command(default_member_permissions=perms)
    async def ignorechannel(self, inter: ApplicationCommandInteraction, channel: disnake.TextChannel = None):
        if channel is None:
            channel = inter.channel
        if channel.id not in self.bot.ignoredChannels:
            self.bot.ignoredChannels.append(channel.id)
        else:
            self.bot.ignoredChannels.remove(channel.id)
        embed = Embed(description="Channel " + channel.mention + " will " + ("now" if channel.id in self.bot.ignoredChannels else "no longer") + " be ignored")
        with open("elems.sav", "wb") as file:
            pickle.dump([self.bot.doLog, self.bot.logChannel.id if self.bot.logChannel else None, self.bot.ignoredChannels], file)
        await inter.response.send_message(embed=embed)