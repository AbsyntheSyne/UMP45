import pickle

import disnake
from disnake import Permissions, ApplicationCommandInteraction, Embed
from disnake.ext.commands import Cog, slash_command

perms = Permissions(8)


def saveToPickle(bot):
    with open("elems.sav", "wb") as file:
        pickle.dump([bot.doLog, bot.logChannel.id if bot.logChannel else None, bot.ignoredChannels, bot.muteRole if bot.muteRole else None], file)


class CommandCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(default_member_permissions=perms)
    async def dolog(self, inter: ApplicationCommandInteraction):
        self.bot.doLog = not self.bot.doLog
        yesNoLog = "now" if self.bot.doLog else "no longer"
        channelName = ((" in the channel #" + self.bot.logChannel.name) if self.bot.logChannel else " as soon as you configure a channel using /logchannel")
        embed = Embed(description="The bot will " + yesNoLog + " log" + channelName)
        saveToPickle(self.bot)
        await inter.response.send_message(embed=embed)

    @slash_command(default_member_permissions=perms)
    async def logchannel(self, inter: ApplicationCommandInteraction, channel: disnake.TextChannel = None):
        if channel is None:
            self.bot.logChannel = inter.channel
        else:
            self.bot.logChannel = channel
        embed = Embed(description="The logging channel has been set to #" + self.bot.logChannel.name)
        saveToPickle(self.bot)
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
        saveToPickle(self.bot)
        await inter.response.send_message(embed=embed)

    @slash_command(default_member_permissions=perms)
    async def ban(self, inter: ApplicationCommandInteraction, user: disnake.Member, reason: str = None):
        await user.ban(reason=reason)
        embed = Embed(description="User " + user.mention + " has been banned")
        await inter.response.send_message(embed=embed)

    @slash_command(default_member_permissions=perms)
    async def kick(self, inter: ApplicationCommandInteraction, user: disnake.Member, reason: str = None):
        await user.kick(reason=reason)
        embed = Embed(description="User " + user.mention + " has been kicked")
        await inter.response.send_message(embed=embed)

    @slash_command(default_member_permissions=perms)
    async def unban(self, inter: ApplicationCommandInteraction, user: disnake.User, reason: str = None):
        await inter.guild.unban(user, reason=reason)
        embed = Embed(description="User " + user.mention + " has been unbanned")
        await inter.response.send_message(embed=embed)

    @slash_command(default_member_permissions=perms)
    async def muterole(self, inter: ApplicationCommandInteraction, role: disnake.Role):
        self.bot.muteRole = role.id
        embed = Embed(description="The mute role has been set to " + role.mention)
        saveToPickle(self.bot)
        await inter.response.send_message(embed=embed)

    @slash_command(default_member_permissions=perms)
    async def mute(self, inter: ApplicationCommandInteraction, user: disnake.Member, reason: str = None):
        if self.bot.muteRole is None:
            embed = Embed(description="You must set a mute role first using /muterole")
            await inter.response.send_message(embed=embed)
            return
        await user.add_roles(inter.guild.get_role(self.bot.muteRole.id), reason=reason)
        embed = Embed(description="User " + user.mention + " has been muted")
        await inter.response.send_message(embed=embed)

    @slash_command(default_member_permissions=perms)
    async def unmute(self, inter: ApplicationCommandInteraction, user: disnake.Member, reason: str = None):
        if self.bot.muteRole is None:
            embed = Embed(description="You must set a mute role first using /muterole")
            await inter.response.send_message(embed=embed)
            return
        elif inter.guild.get_role(self.bot.muteRole.id) not in user.roles:
            embed = Embed(description="User " + user.mention + " is not muted")
            await inter.response.send_message(embed=embed)
            return
        await user.remove_roles(inter.guild.get_role(self.bot.muteRole.id), reason=reason)
        embed = Embed(description="User " + user.mention + " has been unmuted")
        await inter.response.send_message(embed=embed)

    @slash_command(default_member_permissions=perms)
    async def clear(self, inter: ApplicationCommandInteraction, amount: int, user: disnake.Member = None):
        if user is not None:
            await inter.channel.purge(limit=amount, check=lambda message: message.author.id == user.id)
            embed = Embed(description=str(amount) + " messages from " + user.mention + " have been deleted")
            await inter.response.send_message(embed=embed)
        else:
            await inter.channel.purge(limit=amount)
            embed = Embed(description=str(amount) + " messages have been deleted")
            await inter.response.send_message(embed=embed)
