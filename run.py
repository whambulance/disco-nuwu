import uwuify
import discord
from discord.ext import commands
import os
import asyncio

dir_path = os.path.dirname(os.path.realpath(__file__))
flags = uwuify.SMILEY | uwuify.YU
token = open(dir_path + "\\bot.token", mode="r").read()
client = discord.Client()

embed = discord.Embed(
    description="Degenerate-ize your messages!",
    color=0x4103FC,
)
embed.set_author(
    name="disco-nuwu",
    url="https://github.com/whambulance/disco-nuwu",
    icon_url="https://images.discordapp.net/avatars/689333255870480503/df4d10cc3f7027f13198f17ca3637173.png?size=512",
)
embed.add_field(
    name="!uwu",
    value=("Add !uwu before your message to have me delete and" " resend it!"),
)
embed.add_field(
    name="Add a reaction",
    value=(
        "Add the :fox: or :wolf: reaction to have a message"
        " reposted by this degenerate bot"
    ),
)


def uwu_str(message: str) -> str:
    message = message.replace("!uwu ", "").replace("!uwu", "")
    message = discord.utils.escape_markdown(message)
    message = discord.utils.escape_mentions(message)
    return uwuify.uwu(message, flags=flags)


@client.event
async def on_ready():
    gameactivity = discord.Game("!uwuhelp whats this?")
    await client.change_presence(activity=gameactivity)
    print(f"Connected to bot: {client.user.name}")
    print(f"Bot ID: {client.user.id}")


@client.event
async def on_message(message):
    if message.author.bot:
        exit
    channel = message.channel
    author = message.author
    botmember = message.guild.get_member_named(str(message.guild.me))
    botname = uwu_str(author.nick) if author.nick else uwu_str(author.name)

    if message.content.startswith("!uwu "):
        uwumessage = uwu_str(message.content)
        await botmember.edit(nick=botname)
        await channel.send(uwumessage)
        await botmember.edit(nick=None)

    elif message.content.startswith("!uwuhelp"):
        await channel.send(embed=embed)

    else:

        def check(reaction, user):
            return (
                user == message.author
                and reaction.message == message
                and str(reaction.emoji) in ["🦊", "🐺"]
            )

        try:
            reaction, user = await client.wait_for(
                "reaction_add", timeout=120.0, check=check
            )
        except asyncio.TimeoutError:
            pass
        else:
            uwumessage = uwu_str(message.content)
            await channel.send(uwumessage)


# This doesn't work but I wish it did because it's less memory intensive than
# the current solution
# @client.event
# async def on_reaction_add(reaction, user):
#     if reaction.message.author.bot:
#         exit
#     channel = reaction.message.channel
#     if str(reaction.emoji) in ["🦊", "🐺"]:
#         counter = 0
#         for e in reaction.message.reactions:
#             if "🦊" in e.emoji or "🐺" in e.emoji:
#                 counter += 1
#                 if e.count > 1:
#                     exit
#         if counter > 1:
#             exit
#         newmessage = esc_formatting(reaction.message.content)
#         uwumessage = uwuify.uwu(newmessage, flags=flags)
#         sentmessage = await channel.send(uwumessage)


client.run(token)
