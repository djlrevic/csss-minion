#pylint: disable=C
import discord
from discord.ext import commands

FROZEN_ROLES = [228765603756900352, 289285166436843521, 314296819272122368, 296466915235332106, 228985701792743424, 229014335299649536]

class Classes():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def newclass(self, ctx, course):
        """Create a new discord class/role
        Usage: newclass <someclass>
        Creating a class/role places you in that class/role
        """

        course = course.lower()
        dupe = False
        for j in range(0, len(ctx.message.server.roles)):
            if ctx.message.server.roles[j].name == course:
                dupe = True
        if dupe == True:
            await self.bot.say("Class already exists")
        else:
            # temp value
            flag = True
            # temp value

            # flag = False
            # for i in range(0, len(ctx.message.author.roles)):
            #     if ctx.message.author.roles[i].name == "Regular":
            #         flag = True
            if flag == True:
                newRole = await self.bot.create_role(ctx.message.server, name = course, mentionable = True)# , hoist = True)
                await self.bot.add_roles(ctx.message.author, newRole)
                await self.bot.say(course+" class has been created. You have been placed in it.")
            else:
                await self.bot.say("You need to be level 10 and above to create classes! My master said this is to reduce spam.")

    @commands.command(pass_context = True)
    async def whois(self, ctx, course):
        """List people in a discord class/role
        Usage: whois <someclass>
        """
        get = 0
        for i in ctx.message.server.roles:
            if i.name == course:
                get = i
        if get == 0:
            # not role specified not found
            await self.bot.say("That course doesn't exist!")
        else:
            # role specified is found
            # await self.bot.say("Found {}".format(get.name))
            people = []
            for i in ctx.message.server.members:
                if get in i.roles:
                    if i.nick == None:
                        people.append(i.name)
                    else:
                        people.append(i.nick)
            if len(people) == 0:
                # no users found in that group
                await self.bot.say("No one in this group!")
            else:
                result = "```I found these people: \n \n"
                for i in people:
                    result += str(i) + "\n"
                result += "```"
                await self.bot.say(result)

    # Remove user from role
    @commands.command(pass_context = True)
    async def iamn(self, ctx, course : str):
        """Remove yourself from a discord class/role
        Usage: iamn <someclass>
        """
        course = course.lower()
        found = 0
        for i in range(0, len(ctx.message.author.roles)):
            if course == ctx.message.author.roles[i].name:
                found = i
        if found == 0:
            await self.bot.say("You are not currently in this class.")
        else:
            await self.bot.remove_roles(ctx.message.author, ctx.message.author.roles[found])
            await self.bot.say("You've been removed from " + course)

    @commands.command(pass_context = True)
    async def iam(self, ctx, course : str):
        """Place yourself into a discord class/role
        Usage: iam <someclass>
        """
        course = course.lower()
        for role in ctx.message.server.roles:
            if course == role.name:
                # found a match
                if int(role.id) in FROZEN_ROLES:
                    await self.bot.say("This role is locked.")
                    return
                else:
                    print(role.id)
                    await self.bot.add_roles(ctx.message.author, role)
                    await self.bot.say("You've been placed in "+ course)
                    return
        await self.bot.say("This class doesn't exist. Try creating it with .newclass name")

def setup(bot):
    bot.add_cog(Classes(bot))
