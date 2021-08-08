# Functions related to Discord server events (not API events)
import discord, db
from config import client, JUNIMO_ROLE, VERIFY_EVENT, HIDDEN_EVENTS

AWARD_DICT = {'1️⃣': 1, '2️⃣': 5, '3️⃣': 10}

async def award_event_prize(payload):
    # Only give reward if giver is an admin, and correct emoji was used
    # Can't use requires_admin wrapper as there is no message object from the event
    user_roles_ids = [x.id for x in payload.member.roles]
    if JUNIMO_ROLE in user_roles_ids:
        emoji_name = payload.emoji if type(payload.emoji) == str else payload.emoji.name
        if emoji_name in AWARD_DICT and payload.channel_id == VERIFY_EVENT:
            # Need to know what server this is
            server = [x for x in client.guilds if x.id == payload.guild_id][0]
            channel = discord.utils.get(server.channels, id=payload.channel_id)
            try:
                author = None
                message = await channel.fetch_message(payload.message_id)
                # Need to check if we are reacting to an archived post by ourselves
                if message.author == client.user and len(message.mentions) == 1:
                    author = message.mentions[0]
                else:
                    author = message.author

                # Give the team their points for submitting
                team = db.get_team(author.id)
                db.add_points(team, AWARD_DICT[emoji_name])

                # Add our own emoji, so we can show that it went through
                await message.add_reaction(payload.emoji)

            except Exception as e:
                print(f"Exception found when fetching reaction message: {str(e)}")

async def event_check(message):
    await _check_hidden_task(message)

async def _check_hidden_task(message):
    # For events where other members shouldn't see entries we need to:
    # - Do basic checking to see if this is valid entry
    # - Delete their post in chat
    # - Ping them with a thumbs up, showing their entry was received
    # - Repost into hidden channel for staff member to approve later

    # If this isn't a valid event channel, leave
    if message.channel.id not in HIDDEN_EVENTS:
        return

    # Limit to image/videos
    files = [await a.to_file() for a in message.attachments if a.height]

    if files:
        validation_channel = discord.utils.get(message.guild.text_channels, id=VERIFY_EVENT)
        if validation_channel:
            await validation_channel.send(f"Entry from <@{message.author.id}> in <#{message.channel.id}>", files=files)
            await message.channel.send(f"<@{message.author.id}> :thumbsup:")

    # Valid entry or not, we want to delete it
    await message.delete()
