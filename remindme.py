import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
import re
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
scheduler = AsyncIOScheduler()
scheduler.start()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='remind')
async def remind(ctx, member: discord.Member, time: str, *, message: str):
    print("Received reminder request...")
    time_pattern = re.compile(r'(\d+)([smhd])')
    match = time_pattern.match(time)
    if not match:
        await ctx.send("Invalid time format! Use a number followed by 's', 'm', 'h', or 'd' (e.g., 10s, 5m, 2h, 1d).")
        return

    amount, unit = int(match.group(1)), match.group(2)
    now = datetime.now()

    if unit == 's':
        reminder_time = amount
    elif unit == 'm':
        reminder_time = amount * 60
    elif unit == 'h':
        reminder_time = amount * 3600
    elif unit == 'd':
        reminder_time = amount * 86400

    print(f"Reminder set for {reminder_time} seconds.")

    await asyncio.sleep(reminder_time)
    await ctx.send(f"{member.mention}: {message}")

async def send_reminder(member, message):
    print("Sending reminder...")
    await member.send(f"{member.mention}: {message}")

@bot.command(name='remind_help')
async def help_command(ctx):
    help_msg = """
    **Reminder Bot Commands:**
    `/remind @user <time> <message>`
    Set a reminder for a user.
    `<time>` can be in seconds (s), minutes (m), hours (h), or days (d)
    Example: `/remind @Cookie 2m Don't forget to eat!`
    """
    await ctx.send(help_msg)

print("Starting the bot...")
bot.run('YOUR_BOT_TOKEN_HERE')

