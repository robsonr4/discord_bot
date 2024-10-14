from discord import  Interaction, ButtonStyle
from discord.utils import get
from discord.ui import View, Button


class TagsButton(View):
    def __init__(self, roles):
        super().__init__(timeout=None)
        for role in roles:
            self.add_item(Button(label=role, style=ButtonStyle.primary, custom_id=f"role_{role}"))

    async def interaction_check(self, interaction: Interaction) -> bool:
        custom_id = interaction.data["custom_id"]
        if custom_id.startswith("role_"):
            role_name = custom_id[5:]  # Remove "role_" prefix
            role = get(interaction.guild.roles, name=role_name)
            if role:
                await interaction.user.add_roles(role)
                print(interaction.user.get_role(get(interaction.guild.roles, name="Participant").id))
                await interaction.response.send_message(f"Added role {role_name} to {interaction.user.mention}", ephemeral=True)
            else:
                await interaction.response.send_message(f"Role {role_name} not found", ephemeral=True)
        return True