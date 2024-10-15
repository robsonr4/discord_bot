from discord import Interaction, TextChannel, Guild, Role, CategoryChannel
from discord.utils import get
from const import TAGS_ROLES


async def tags_interaction(interaction: Interaction) -> bool:
    """
    Handle the tags interaction.

    PARAMETERS:
        interaction: Interaction:
            The interaction to handle.

    RETURNS:
        bool:
            Whether the interaction was handled.
    """

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
    """
    Create a role.

    PARAMETERS:
        guild: Guild:
            The guild to create the role in.
        role_name: str:
            The name of the role to create.

    RETURNS:
        Role:
            The created role.
    """
    role = get(guild.roles, name=role_name)
    if not role:
        role = await guild.create_role(name=role_name)
    return role

async def create_category(guild: Guild, category_name: str) -> CategoryChannel:
    """
    Create a category.

    PARAMETERS:
        guild: Guild:
            The guild to create the category in.
        category_name: str:
            The name of the category to create.

    RETURNS:
        CategoryChannel:
            The created category.
    """
    category = get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(name=category_name)
    return category

async def create_channel(guild: Guild, channel_name: str, category: CategoryChannel) -> TextChannel:
    """
    Create a channel.

    PARAMETERS:
        guild: Guild:
            The guild to create the channel in.
        channel_name: str:
            The name of the channel to create.
        category: CategoryChannel:
            The category to create the channel in.
        category_name: str:
            The name of the category to create.

    RETURNS:
        TextChannel:
            The created channel.
    """
    channel = get(category.text_channels, name=channel_name.lower())
    if not channel:
        channel = await guild.create_text_channel(name=channel_name, category=category)
    return channel


