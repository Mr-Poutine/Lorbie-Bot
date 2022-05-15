from discord.ext import commands
from discord import Intents
import discord
import os
from dotenv import load_dotenv

load_dotenv()

intents = Intents.default()
intents.message_content = True


class Bot(commands.Bot):
	def __init__(self, **kwargs):
		super().__init__(command_prefix=commands.when_mentioned_or('?lorb'),
                         intents=intents,
                         case_insensitive=True,
                         **kwargs)

	async def setup_hook(self):
		for i in next(os.walk(os.getcwd() + "/cogs"),
                      (None, None, []))[2][::-1]:
			try:
				await self.load_extension("cogs." + i[:-3])
			except Exception as exc:
				print(
                    f'Could not load extension {i[:-3]} due to {exc.__class__.__name__}: {exc}'
                )

	async def on_ready(self):
		print(f'Logged on as {self.user} (ID: {self.user.id})')

	async def on_message(self, message: discord.Message):
		print(f"message: {message.content}, author: {message.author}, interaction: {message.interaction}")

		if(message.interaction):
			await message.channel.send(f"The above was an interaction, answered by {message.author.mention} and called by {message.interaction.user.mention}")
		
		await self.process_commands(message)


bot = Bot()


#command list
@bot.command(name="hello")
async def hello(ctx: commands.Context):
    await ctx.reply(f"Hello {ctx.author.mention}")


@bot.command(name="test")
async def test(ctx: commands.Context):
    await ctx.reply(f"this is a test, {ctx.author.mention}")


bot.run(os.getenv("BOT_TOKEN"))
