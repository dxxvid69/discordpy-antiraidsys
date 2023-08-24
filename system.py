import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.member_join = True  # Enable member join events

bot = commands.Bot(command_prefix="!", intents=intents)

# Your server's threshold for triggering anti-raid
RAID_MEMBER_THRESHOLD = 5

# Dictionary to keep track of members who joined recently
recently_joined = {}

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.id not in recently_joined:
        recently_joined[guild.id] = []
    
    recently_joined[guild.id].append(member.id)
    await check_raid(guild)

@bot.event
async def on_member_remove(member):
    guild = member.guild
    if guild.id in recently_joined and member.id in recently_joined[guild.id]:
        recently_joined[guild.id].remove(member.id)

async def check_raid(guild):
    if guild.id in recently_joined:
        if len(recently_joined[guild.id]) >= RAID_MEMBER_THRESHOLD:
            await guild.owner.send("Possible raid detected in your server!")
            # Take appropriate action here, such as banning members, etc.
    
    recently_joined[guild.id] = []

bot.run("YOUR_BOT_TOKEN")

# In this code, we're using the `on_member_join` and `on_member_remove` events to keep track of recently joined members. When a member joins, they're added to the list of recently joined members for that guild. When a member leaves, they're removed from the list.

# The `check_raid` function is called whenever a new member joins. If the number of recently joined members exceeds the threshold, it sends a message to the server owner indicating a possible raid. You can customize this function to take further actions like banning or kicking members.

# Please note that this is a simplified example and doesn't cover all aspects of an anti-raid system. Depending on your needs, you might want to add more features like rate limiting, monitoring patterns, and more. Also, remember to replace `"YOUR_BOT_TOKEN"` with your actual bot token.
