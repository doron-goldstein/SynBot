from discord.ext import commands
import discord
import os
import asyncio
import inspect
import textwrap
import tokage


class Utilities:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, enabled=False)
    async def setavatar(self, ctx, picture):
        path = os.path.join("Bot Pics", picture)
        try:
            with open('%s' % path, 'rb') as f:
                await ctx.bot.user.edit(avatar=f.read())
            await ctx.send(":ok_hand: Avatar changed to %s" % picture.split(".")[0])
        except Exception:
            await ctx.send(":exclamation: File not found!")

    @commands.command(hidden=True, aliases=["eval", "evaluate"])
    @commands.is_owner()
    async def debug(self, ctx, *, code: str):
        """Evaluates code."""
        code = code.strip('`')
        python = '```py\n{}\n```'
        result = None

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.guild,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            'history': await ctx.channel.history().flatten(),
            't_client': tokage.Client()
        }

        env.update(globals())

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.send(python.format(type(e).__name__ + ': ' + str(e)))
            return

        await ctx.send(python.format(result))

    @commands.command(name="exec", hidden=True)
    @commands.is_owner()
    async def execute(self, ctx, *, code):
        if code.startswith("```") and code.endswith("```"):
            code = code.strip("```")
            if code.startswith("py\n"):
                code = code[3:]
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.guild,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            'history': await ctx.channel.history().flatten(),
            't_client': tokage.Client()
        }
        env.update(globals())
        wrapped = 'async def func():\n%s' % textwrap.indent(code, '  ')
        try:
            result = exec(wrapped, env)
            func = env['func']
            await func()
            if result:
                await ctx.send(f"```{result}```")
        except Exception as e:
            await ctx.send(f"```{type(e).__name__ + ': ' + str(e)}```")

    @commands.command(aliased=["join", "inv"])
    async def invite(self, ctx):
        """Sends an invite link for the bot"""
        await ctx.send(f"<{discord.utils.oauth_url(self.bot.user.id)}>")
def setup(bot):
    bot.add_cog(Utilities(bot))
