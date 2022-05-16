from datetime import datetime
from enum import Enum
import time
from discord.ext import commands, tasks
import discord

from constants import OwOID


class ReminderType(Enum):

    owoHunt = 1
    owoBattle = 2


class Reminder:

    def __init__(self, reminderType: ReminderType, user: discord.User, channel: discord.TextChannel):
        self.reminderType = reminderType
        self.user = user
        self.channel = channel

    def getReminder(self):

        if(self.reminderType == ReminderType.owoHunt):
            return f"{self.user.mention}, its time to OwO Hunt"

        elif(self.reminderType == ReminderType.owoBattle):
            return f"{self.user.mention}, its time to OwO Battle"


class Timers(commands.Cog):
    """The description for Timers goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.timers: dict = {}

        self.checkReminders.start()

    def addReminder(self, duration: int, reminder: Reminder):

        reminderTime = int(time.time()) + duration

        if reminderTime not in self.timers:
            self.timers[reminderTime] = []

        self.timers[reminderTime].append(reminder)

    def checkOwOTimer(self, interaction: discord.MessageInteraction, channel: discord.TextChannel):
        if interaction.name == "hunt":
            self.addReminder(15, Reminder(
                ReminderType.owoHunt, interaction.user, channel))

        elif interaction.name == "battle":
            self.addReminder(15, Reminder(
                ReminderType.owoBattle, interaction.user, channel))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if(message.interaction):
            if(message.author.id == OwOID):
                self.checkOwOTimer(message.interaction, message.channel)

    @tasks.loop(seconds=1)
    async def checkReminders(self):

        keysToRemove = []

        for key in self.timers:

            if key <= int(time.time()):
                keysToRemove.append(key)
                for reminder in self.timers[key]:
                    reminder: Reminder = reminder
                    await reminder.channel.send(reminder.getReminder())

        for key in keysToRemove:
            self.timers.pop(key)

    @checkReminders.before_loop
    async def beforeCheckReminder(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Timers(bot))
