from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, Member, Role, Embed, TextChannel, Color, Guild, PermissionOverwrite, Interaction, ButtonStyle, InteractionType
from discord.utils import get
from responses import get_response
from const import MESSAGES
import asyncio
from modals import TagsButton

# ENV setup
load_dotenv()
TOKEN: Final = os.getenv("DISCORD_TOKEN")

# BOT setup
intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
client: Client = Client(intents=intents)

# TAGS HANDLER
@client.event
async def on_interaction(interaction: Interaction) -> None:
    if interaction.type == InteractionType.component:
        print("HERE 1")
        print(interaction.data)
        if interaction.data["custom_id"] == "role_JS":
            print("HERE 2")
            await interaction.user.add_roles(get(interaction.guild.roles, name="JS"))
            await interaction.response.send_message(f"Added role JS to {interaction.user.mention}", ephemeral=True)
            print("HERE 3")
# NEW MEMBER HANDLER
@client.event
async def on_member_join(member: Member) -> None:
    print(f"{member} has joined the server.")
    await member.send("Welcome to the server!")
    
    # Add role
    # role: Role = get(member.guild.roles, name="New Member")
    # await member.add_roles(role)
    # print(f"Added role {role.name} to {member.name}")
    # await member.send(f"You have been added to the {role.name} role.")

    # Create private channel
    guild: Guild = member.guild
    channel: TextChannel = await guild.create_text_channel(
        "secret",
        topic="This is an onboarding channel. In order to get access to the rest of the server, you must complete the onboarding process.",
        overwrites={
            member: PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True, send_messages_in_threads=True),
            guild.default_role: PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False, send_messages_in_threads=False),
            guild.me: PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True, send_messages_in_threads=True)
        } 
        )
    await channel.edit(name=f"onboarding-{member.name}")
    await channel.send(f"Welcome to the server, {member.mention}!")
    rules_embed: Embed = Embed(
        title="Rules",
        description=MESSAGES["RULES_ACKNOWLEDGEMENT"],
        color=Color.blue()
    )
    await channel.send(embed=rules_embed)






    


# MESSAGE HANDLER
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("No message received")
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# HANDLE STARTUP
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")

# HANDLE INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    channel_name: str = message.channel.name
    if channel_name.startswith("onboarding-"):
        
        if user_message := message.content.lower() == "i acknowledge the rules":
            await message.channel.send(MESSAGES["RULES_ACKNOWLEDGEMENT_CONFIRMATION"])
            
            # Wait for 5 seconds
            await asyncio.sleep(5)
            await message.author.add_roles(get(message.guild.roles, name="Participant"))
            await message.channel.delete()
            return
    elif channel_name == "🔖│tags│🔖":
        return
    elif channel_name == "botcontrol":
        if user_message := message.content.lower() == "!send-tags":
            tags_channel: TextChannel = get(message.guild.channels, name="🔖│tags│🔖")
            embed: Embed = Embed(
                title=MESSAGES["TAGS_TITLE"],
                description=MESSAGES["TAGS_DESCRIPTION"],
                color=Color.blue()
            )
            roles = ["JS", "Python", "Java", "C++", "Ruby", "PHP"]  # Add all your desired roles here
            await tags_channel.send(embed=embed, view=TagsButton(roles=roles))
            return


    
    
    username: str = str(message.author)
    user_message: str = str(message.content)
    channel: str = str(message.channel)

    print(f"{username} said: '{user_message}' ({channel})")
    await send_message(message, user_message)

# MAIN
def main() -> None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()

