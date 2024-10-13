from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# ENV setup
load_dotenv()
TOKEN: Final = os.getenv('DISCORD_TOKEN')

# BOT setup
intents: Intents = Intents.default()
intents.message_content = True