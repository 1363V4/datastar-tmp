import os

from twitchio.ext import commands
import requests
from dotenv import load_dotenv

load_dotenv()

# Replace these with your bot's credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BOT_ID = os.getenv('BOT_ID')
OWNER_ID = os.getenv('OWNER_ID')

# URL to send the POST request to
TARGET_URL = 'https://tmp.leg.ovh/bot'

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_ID,
            owner_id=OWNER_ID,
            prefix="!",
        )

    async def event_ready(self):
        print(f'Logged in as {self.nick}')

    @commands.command(name='bot')
    async def trigger_command(self, ctx: commands.Context):
        try:
            # Send a POST request to the target URL
            response = requests.post(TARGET_URL)
            if response.status_code == 200:
                await ctx.send(f'Successfully triggered the endpoint! Response: {response.text}')
            else:
                await ctx.send(f'Failed to trigger the endpoint. Status code: {response.status_code}')
        except Exception as e:
            await ctx.send(f'An error occurred: {str(e)}')

# Run the bot
bot = Bot()
bot.run()
