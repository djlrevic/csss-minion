import asyncio
import discord

class CannotPaginate(Exception):
    pass

class Pages:
    def __init__(self, bot, *, message, ctx, entries, per_page=12):
        self.bot = bot
        self.entries = entries
        self.message = message
        self.author = message.author
        self.per_page = per_page
        pages, left_over = divmod(len(self.entries), self.per_page)
        if left_over:
            pages += 1
        self.maximum_pages = pages
        self.embed = discord.Embed()
        self.paginating = len(entries) > per_page
        self.reaction_emojis = [
            ('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self.first_page),
            ('\N{BLACK LEFT-POINTING TRIANGLE}', self.previous_page),
            ('\N{BLACK RIGHT-POINTING TRIANGLE}', self.next_page),
            ('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self.last_page),
            ('\N{INPUT SYMBOL FOR NUMBERS}', self.numbered_page ),
            ('\N{BLACK SQUARE FOR STOP}', self.stop_pages),
            ('\N{INFORMATION SOURCE}', self.show_help),
        ]

        guild = self.message.guild
        if guild is not None:
            self.permissions = self.message.channel.permissions_for(guild.me)
        else:
            self.permissions = self.message.channel.permissions_for(self.bot.user)

        if not self.permissions.embed_links:
            raise CannotPaginate('Bot does not have embed links permission.')


    def get_page(self, page):
        base = (page - 1) * self.per_page
        return self.entries[base:base + self.per_page]

    async def show_page(self, page, *, first=False, ctx):
        self.current_page = page
        entries = self.get_page(page)
        p = []
        for t in entries:
            p.append(t)

        self.embed.set_footer(text='Page %s/%s (%s entries)' % (page, self.maximum_pages, len(self.entries)))

        if not self.paginating:
            self.embed.clear_fields()
            for i in p:
                self.embed.add_field(name = i[0], value = i[1])
            return await ctx.send( embed=self.embed)

        if not first:
            self.embed.clear_fields()
            for i in p:
                self.embed.add_field(name = i[0], value = i[1])
            await self.bot.edit_message(self.message, embed=self.embed)
            return

        # verify we can actually use the pagination session
        if not self.permissions.add_reactions:
            raise CannotPaginate('Bot does not have add reactions permission.')

        if not self.permissions.read_message_history:
            raise CannotPaginate('Bot does not have Read Message History permission.')

        self.embed.description = 'Confused? Press with \N{INFORMATION SOURCE} for more info.'

        self.embed.clear_fields()
        for i in p:
            self.embed.add_field(name = i[0], value = i[1])
        self.message = await self.bot.send_message(self.message.channel, embed=self.embed)
        for (reaction, _) in self.reaction_emojis:
            if self.maximum_pages == 2 and reaction in ('\u23ed', '\u23ee'):
                # no |<< or >>| buttons if we only have two pages
                # we can't forbid it if someone ends up using it but remove
                # it from the default set
                continue

            await self.bot.add_reaction(self.message, reaction)

    async def checked_show_page(self, page, ctx):
        if page != 0 and page <= self.maximum_pages:
            await self.show_page(page)

    async def first_page(self, ctx):
        """goes to the first page"""
        await self.show_page(1, ctx)

    async def last_page(self, ctx):
        """goes to the last page"""
        await self.show_page(self.maximum_pages, ctx)

    async def next_page(self, ctx):
        """goes to the next page"""
        await self.checked_show_page(self.current_page + 1, ctx)

    async def previous_page(self, ctx):
        """goes to the previous page"""
        await self.checked_show_page(self.current_page - 1, ctx)

    async def show_current_page(self, ctx):
        if self.paginating:
            await self.show_page(self.current_page, ctx)

    async def numbered_page(self, ctx):
        """lets you type a page number to go to"""
        to_delete = []
        to_delete.append(await self.bot.send_message(self.message.channel, 'What page do you want to go to?'))
        msg = await self.bot.wait_for_message(author=self.author, channel=self.message.channel,
                                              check=lambda m: m.content.isdigit(), timeout=30.0)
        if msg is not None:
            page = int(msg.content)
            to_delete.append(msg)
            if page != 0 and page <= self.maximum_pages:
                await self.show_page(page, ctx)
            else:
                to_delete.append(await self.bot.say('Invalid page given. (%s/%s)' % (page, self.maximum_pages)))
                await asyncio.sleep(5)
        else:
            to_delete.append(await self.bot.send_message(self.message.channel, 'Took too long.'))
            await asyncio.sleep(5)

        try:
            await self.bot.delete_messages(to_delete)
        except Exception:
            pass

    async def show_help(self):
        """shows this message"""
        e = discord.Embed()
        messages = ['Welcome to the interactive paginator!\n']
        messages.append('This interactively allows you to see pages of text by navigating with ' \
                        'reactions. They are as follows:\n')

        for (emoji, func) in self.reaction_emojis:
            messages.append('%s %s' % (emoji, func.__doc__))

        e.description = '\n'.join(messages)
        e.colour =  0x738bd7 # blurple
        e.set_footer(text='We were on page %s before this message.' % self.current_page)
        await self.bot.edit_message(self.message, embed=e)

        async def go_back_to_current_page():
            await asyncio.sleep(60.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

    async def stop_pages(self):
        """stops the interactive pagination session"""
        await self.bot.delete_message(self.message)
        self.paginating = False

    def react_check(self, reaction, user):
        if user is None or user.id != self.author.id:
            return False

        for (emoji, func) in self.reaction_emojis:
            if reaction.emoji == emoji:
                self.match = func
                return True
        return False

    async def paginate(self):
        """Actually paginate the entries and run the interactive loop if necessary."""
        await self.show_page(1, first=True)

        while self.paginating:
            react = await self.bot.wait_for_reaction(message=self.message, check=self.react_check, timeout=120.0)
            if react is None:
                self.paginating = False
                try:
                    await self.bot.clear_reactions(self.message)
                except:
                    pass
                finally:
                    break

            try:
                await self.bot.remove_reaction(self.message, react.reaction.emoji, react.user)
            except:
                pass # can't remove it so don't bother doing so

            await self.match()