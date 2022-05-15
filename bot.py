from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

load_dotenv()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('?lorb'), **kwargs)

    async def setup_hook(self):
        for i in next(os.walk(os.getcwd() + "/cogs"), (None, None, []))[2][::-1]:
            try:
                await self.load_extension("cogs." + i[:-3])
            except Exception as exc:
                print(
                    f'Could not load extension {i[:-3]} due to {exc.__class__.__name__}: {exc}')

    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')


bot = Bot()

# write general commands here

bot.run(os.getenv("BOT_TOKEN"))
