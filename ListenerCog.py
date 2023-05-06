import disnake
from disnake.ext.commands import Cog
from disnake import Embed


class ListenerCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        if self.bot.logChannel is None or self.bot.doLog is False or message.channel.id in self.bot.ignoredChannels:
            return
        embed = Embed(
            title=":wastebasket: Message deleted in #" + message.channel.name,
            description=message.author.mention + " (" + message.author.name + "#" + message.author.discriminator + ")")
        embed.set_footer(text="sent at " + message.created_at.strftime("%m/%d/%Y, %H:%M:%S"))
        embed.add_field("Content", message.content, inline=False)
        embed.add_field("ID", str(message.id), inline=False)
        embed.add_field("Channel", message.channel.mention + " (" + message.channel.name + ")", inline=False)
        attachmentStr = ""
        for attachment in message.attachments:
            attachmentStr += attachment.url + " (" + attachment.size + "b)\n\n"
        if len(attachmentStr) > 0:
            embed.add_field("Attachments", attachmentStr, inline=False)
        await self.bot.logChannel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if self.bot.logChannel is None or self.bot.doLog is False or before.channel.id in self.bot.ignoredChannels:
            return
        embed = Embed(
            title=":pencil: Message edited",
            description=before.author.mention + " (" + after.author.name + "#" + after.author.discriminator + ")")
        embed.set_footer(text="edited at " + after.edited_at.strftime("%m/%d/%Y, %H:%M:%S"))
        embed.add_field("Previous content", before.content, inline=False)
        embed.add_field("New content", after.content, inline=False)
        embed.add_field("ID", str(after.id), inline=False)
        embed.add_field("Channel", after.channel.mention + " (" + after.channel.name + ")", inline=False)
        await self.bot.logChannel.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        if self.bot.logChannel is None or self.bot.doLog is False:
            return
        embed = Embed(
            title=":white_check_mark: User joined",
            description=member.mention + " (" + member.name + "#" + member.discriminator + ")")
        embed.set_footer(text=member.joined_at.strftime("%m/%d/%Y, %H:%M:%S"))
        embed.add_field("ID", str(member.id), inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field("Joined Server", member.joined_at.strftime("%m/%d/%Y, %H:%M:%S"))
        embed.add_field("Joined Discord", member.created_at.strftime("%m/%d/%Y, %H:%M:%S"))
        await self.bot.logChannel.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member):
        if self.bot.logChannel is None or self.bot.doLog is False:
            return
        embed = Embed(
            title=":x: User left",
            description=member.name + "#" + member.discriminator)
        embed.add_field("ID", str(member.id), inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field("Joined Discord", member.created_at.strftime("%m/%d/%Y, %H:%M:%S"))
        await self.bot.logChannel.send(embed=embed)

    @Cog.listener()
    async def on_member_ban(self, guild, user):
        if self.bot.logChannel is None or self.bot.doLog is False:
            return
        embed = Embed(
            title=":no_entry_sign: User banned",
            description=user.name + "#" + user.discriminator)
        embed.add_field("ID", str(user.id), inline=False)
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field("Joined Discord", user.created_at.strftime("%m/%d/%Y, %H:%M:%S"))
        await self.bot.logChannel.send(embed=embed)

    @Cog.listener()
    async def on_member_unban(self, guild, user):
        if self.bot.logChannel is None or self.bot.doLog is False:
            return
        embed = Embed(
            title=":recycle: User unbanned",
            description=user.name + "#" + user.discriminator)
        embed.add_field("ID", str(user.id), inline=False)
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field("Joined Discord", user.created_at.strftime("%m/%d/%Y, %H:%M:%S"))
        await self.bot.logChannel.send(embed=embed)
