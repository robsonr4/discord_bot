from discord import Interaction, TextChannel, Guild, Role, CategoryChannel
from discord.utils import get
from const import TAGS_ROLES


async def tags_interaction(interaction: Interaction) -> bool:
    tags_channel: TextChannel = get(interaction.guild.channels, name="🔖│tags│🔖")
    custom_id: str = interaction.data["custom_id"]
    if custom_id.startswith("role_"):
        role_name: str = custom_id[5:]  # Remove "role_" prefix
        role = await create_role(interaction.guild, role_name)
        category = await create_category(interaction.guild, "team-building")        
        role_channel = await create_channel(interaction.guild, role_name, category, "team-building")

        if interaction.user.get_role(role.id):
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"Removed role {role_name} from {interaction.user.mention}", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Added role {role_name} to {interaction.user.mention}", ephemeral=True)
        
    return True

async def create_role(guild: Guild, role_name: str) -> Role:
    role = get(guild.roles, name=role_name)
    if not role:
        role = await guild.create_role(name=role_name)
    return role

async def create_category(guild: Guild, category_name: str) -> CategoryChannel:
    category = get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(name=category_name)
    return category

async def create_channel(guild: Guild, channel_name: str, category: CategoryChannel, category_name: str) -> TextChannel:
    category = await create_category(guild, category_name)
    channel = get(category.text_channels, name=channel_name.lower())
    if not channel:
        channel = await guild.create_text_channel(name=channel_name, category=category)
    return channel


