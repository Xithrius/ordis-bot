import secrets
from io import BytesIO
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from discord import Embed, Emoji, File, PartialEmoji, Reaction
from discord.ext.commands import Context as BaseContext
from discord.ext.commands import Group

from bot.constants import CHECKMARK_EMOJI, RESPONSES, Colours

if TYPE_CHECKING:
    from bot.bot import Ordis


class Context(BaseContext):  # pyright: ignore[reportMissingTypeArgument]
    """Definition of a custom context."""

    bot: "Ordis"

    async def check_subcommands(self) -> None:
        if self.invoked_subcommand is not None:
            return

        if not isinstance(self.command, Group):
            raise AttributeError("command is not a group command")

        group: Group[Any, ..., Any] = self.command

        subcommands: list[str] = []

        for cmd in group.commands:
            aliases = ", ".join(cmd.aliases)
            subcommand = f"`{cmd.name} ({aliases})`" if cmd.aliases else f"`{cmd.name}`"
            subcommands.append(subcommand)

        await self.send(
            embed=Embed(
                title="Subcommand not found, try one of these:",
                description="\n".join(subcommands),
            ),
        )

    async def send_image_buffer(
        self,
        buffer: BytesIO,
        *,
        embed: Embed | None = None,
        file_name: str | UUID | None = None,
    ) -> None:
        embed = embed or Embed()
        file_name = file_name or uuid4()

        embed.set_image(url=f"attachment://{file_name}.png")

        file = File(fp=buffer, filename=f"{file_name}.png")

        await self.send(embed=embed, file=file)

    async def done(self, reaction: Emoji | PartialEmoji | Reaction | str = CHECKMARK_EMOJI) -> None:
        await self.message.add_reaction(reaction)

    async def __send_reply_embed(
        self,
        description: str,
        title: str | None,
        color: int,
    ) -> None:
        embed = Embed(
            title=title or RESPONSES[secrets.randbelow(len(RESPONSES))],
            description=description,
            colour=color,
        )

        await self.send(embed=embed)

    async def error_embed(self, description: str, title: str | None = None) -> None:
        await self.__send_reply_embed(
            description,
            title,
            Colours.soft_red,
        )

    async def warning_embed(self, description: str, title: str | None = None) -> None:
        await self.__send_reply_embed(
            description,
            title,
            Colours.soft_orange,
        )

    async def success_embed(self, description: str, title: str | None = None) -> None:
        await self.__send_reply_embed(
            description,
            title,
            Colours.soft_green,
        )
