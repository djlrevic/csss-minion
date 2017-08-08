import discord
from discord.ext import commands

class ModTools:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def lock(self, ctx):
        ch = ctx.message.channel
        ch.permissions_for()

    @commands.command(pass_context=True)
    async def lock(self, ctx):
        if Minion(ctx):
            everyone = ctx.message.server.default_role
            await ch_perms(ctx.message.channel, everyone, False)
            await self.bot.say("Locking Channel")
        else:
            await self.bot.say("You ain't no mod, shoo!")

    @commands.command(pass_context=True)
    async def unlock(self, ctx):
        if Minion(ctx):
            everyone = ctx.message.server.default_role
            await ch_perms(ctx.message.channel, everyone, True)
            await self.bot.say("Unlocking Channel")
        else:
            await self.bot.say("You ain't no mod, shoo!")

    async def ch_perms(self, channel, user, value):
        """Helper function"""
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = value
        await self.bot.edit_channel_permissions(channel, user, overwrite)

    @commands.command(pass_context=True)
    async def unrestrict(self, ctx, *msg):
        """Undo any restrictions on a user for all channels.
        Usage: !unrestrict [users..]
        """
        if Minion(ctx):
            channels = ctx.message.server.channels
            for user in ctx.message.mentions:
                await self.bot.say("Unrestricting user "+user.name)
                for ch in channels:
                    await self.ch_perms(ch, user, None) #None sets to default(inherited) value.
            else:
                await self.bot.say("You ain't no mod, shoo!")

    @commands.command(pass_context=True)
    async def restrict(self, ctx, *msg):
        """Restrict user(s) to only post in certain channels.
        Usage: !restrict [users..] [channels..]
        Example: !restrict @Henry @Roo #offtopic #bottesting

        """
        if Minion(ctx):
            channels = ctx.message.server.channels
            for user in ctx.message.mentions:
                await self.bot.say("Restricting user "+user.name)
                for ch in channels:
                    if ch not in ctx.message.channel_mentions:
                        #print(ch.name,user.nick, "banning user in this channel")
                        #DO NOT PRINT A LIST OF ALL CHANNELS IN PRODUCTION
                        await self.ch_perms(ch, user, False)   #ban user from channel.
                    else:
                        await self.bot.say("You ain't no mod, shoo!")

    def Minion(ctx):
        if "&314296819272122368" in ctx.message.author.roles.id
            return True
        else:
            return False

            def setup(bot):
                bot.add_cog(modtools(bot))
