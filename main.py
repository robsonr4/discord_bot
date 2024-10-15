from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, Member, Embed, TextChannel, Color, Guild, PermissionOverwrite, Interaction, InteractionType
from discord.utils import get
from const import MESSAGES, TAGS_ROLES
import asyncio
from modals import TagsButton
from funcs import tags_interaction, create_role, create_category, create_channel

### CLEANING AND DESCRIPTION TIME

# ENV setup
load_dotenv()
TOKEN: Final = os.getenv("DISCORD_TOKEN")

# BOT setup
intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
client: Client = Client(intents=intents)

# INTERACTIONS HANDLER
@client.event
async def on_interaction(interaction: Interaction) -> None:
    if interaction.type == InteractionType.component and interaction.data["custom_id"].startswith("role_"):
        # When a user clicks a tags button
        await tags_interaction(interaction)

        # update the role count
        custom_id = interaction.data["custom_id"]
        role_name = custom_id[5:]
        role = get(interaction.guild.roles, name=role_name)
        TAGS_ROLES[custom_id] = f"{role_name} ({len(role.members)})"
        await interaction.message.edit(view=TagsButton(roles=TAGS_ROLES))
        


# NEW MEMBER HANDLER
@client.event
async def on_member_join(member: Member) -> None:
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

    # Send welcome message
    await channel.send(f"Welcome to the server, {member.mention}!")

    # Send rules embed
    rules_embed: Embed = Embed(
        title="Rules",
        description=MESSAGES["RULES_ACKNOWLEDGEMENT"],
        color=Color.blue()
    )
    await channel.send(embed=rules_embed)


# HANDLE STARTUP
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")

# HANDLE INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    
    channel_name: str | None = message.channel.name
    
    if channel_name is None:
        return
    
    if channel_name.startswith("onboarding-"):
        # Onboarding message
        if user_message := message.content.lower() == "i acknowledge the rules":
            await message.channel.send(MESSAGES["RULES_ACKNOWLEDGEMENT_CONFIRMATION"])
            
            # Wait for 5 seconds
            await asyncio.sleep(5)
            await message.author.add_roles(get(message.guild.roles, name="Participant"))
            await message.channel.delete()
            await get(message.guild.channels, name="hello").send(f"Welcome to the hackathon, {message.author.mention}!")
            return
    elif channel_name == "botcontrol":
        # Private bot control channel for sending announcements or doing other commands
        if user_message := message.content.lower() == "!send-tags":
            # Restart/send tags
            tags_channel: TextChannel = get(message.guild.channels, name="🔖│tags│🔖")
            guild: Guild = message.guild

            if not tags_channel:
                tags_channel = await create_channel(guild, "🔖│tags│🔖", get(guild.categories, name="botcontrol"))
            
            # delete all messages in channel
            async for msg in tags_channel.history(limit=100):
                await msg.delete()
            
            # update role counts
            for custom_id, label in TAGS_ROLES.items():
                role_name = custom_id[5:]
                
                role = await create_role(guild, role_name)
                category = await create_category(guild, "team-building")
                channel = await create_channel(guild, role_name, category)
                TAGS_ROLES[custom_id] = f"{role_name} ({len(role.members)})"
            
            # send tags embed
            embed: Embed = Embed(
                title=MESSAGES["TAGS_TITLE"],
                description=MESSAGES["TAGS_DESCRIPTION"],
                color=Color.blue()
            )
            await tags_channel.send(embed=embed, view=TagsButton(roles=TAGS_ROLES))
            return


# MAIN
def main() -> None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()

