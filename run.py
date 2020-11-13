import uwuify
import discord
import os
import asyncio

dir_path = os.path.dirname(os.path.realpath(__file__))
flags = uwuify.SMILEY | uwuify.YU
token = open(dir_path + "\\bot.token", mode="r").read()
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)

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
    value=("Add !uwu before your message to have me" " resend it!"),
)
embed.add_field(
    name="!uwud",
    value=("Add !uwud before your message to have me delete and" " resend it!"),
)
embed.add_field(
    name="Add a reaction",
    value=(
        "Add the :fox: or :wolf: reaction to have a message"
        " reposted by this degenerate bot"
    ),
)


def uwu_str(message: str) -> str:
    message = message.replace("!uwu ", "").replace("!uwud ", "")
    message = message.replace("!uwu", "").replace("!uwud", "")
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
        return
    channel = message.channel
    author = message.author
    botmember = message.guild.get_member_named(str(message.guild.me))
    botname = uwu_str(author.nick) if author.nick else uwu_str(author.name)
    msgstart = message.content.split(" ", 1)[0]

    if msgstart in ["!uwu", "!uwud"]:
        uwumessage = uwu_str(message.content)
        if msgstart == ("!uwud"):
            await message.delete()
        await botmember.edit(nick=botname)
        await channel.send(uwumessage)
        await botmember.edit(nick=None)

    elif msgstart == "!uwuhelp":
        await channel.send(embed=embed)


@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author.bot:
        return
    channel = reaction.message.channel
    author = reaction.message.author
    botmember = channel.guild.get_member_named(str(channel.guild.me))
    botname = uwu_str(author.nick) if author.nick else uwu_str(author.name)

    if str(reaction.emoji) in ["🦊", "🐺"]:
        reactions = reaction.message.reactions
        count = sum([i.count for i in reactions if i.emoji in ["🦊", "🐺"]])

        if count <= 1:
            uwumessage = uwu_str(reaction.message.content)
            await botmember.edit(nick=botname)
            sentmessage = await channel.send(uwumessage)
            await botmember.edit(nick=None)

            def check(chk_reaction, chk_user):
                reactions = chk_reaction.message.reactions
                count = sum([1 for i in reactions if i.emoji in ["🦊", "🐺"]])
                return count == 0 and chk_reaction.message == reaction.message

            try:
                reaction, user = await client.wait_for(
                    "reaction_remove", timeout=180.0, check=check
                )
            except asyncio.TimeoutError:
                pass
            else:
                await sentmessage.delete()


client.run(token)
