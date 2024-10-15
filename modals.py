from discord import  Interaction, ButtonStyle
from discord.utils import get
from discord.ui import View, Button
from funcs import tags_interaction
from const import TAGS_ROLES


class TagsButton(View):
    def __init__(self, roles: list[tuple[str, str]]):
        super().__init__(timeout=None)
        for custom_id, label in roles.items():
            self.add_item(Button(label=label, style=ButtonStyle.primary, custom_id=custom_id))
