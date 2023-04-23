import re

from pyrogram import filters

from Obito import DRAGONS, pbot as rose
from Obito.pyrogramee.pyrogroups import karmapositivegrp, karmanegativegrp
from Obito.modules.mongo.karma_mongo import (alpha_to_int, get_karma, get_karmas,
                                   int_to_alpha, is_karma_on, karma_off,
                                   karma_on, update_karma)
from Obito.modules.helper_funsc.chat_status import adminsonly

async def get_user_id_and_usernames(client) -> dict:
    with client.storage.lock, client.storage.conn:
        users = client.storage.conn.execute(
            'SELECT * FROM peers WHERE type in ("user", "bot") AND username NOT null'
        ).fetchall()
    users_ = {}
    for user in users:
        users_[user[0]] = user[3]
    return users_

# Needed
n = "\n"
w = " "
bold = lambda x: f"**{x}:** "
bold_ul = lambda x: f"**--{x}:**-- "
mono = lambda x: f"`{x}`{n}"
def section(
    title: str,
    body: dict,
    indent: int = 2,
    underline: bool = False,
) -> str:

    text = (bold_ul(title) + n) if underline else bold(title) + n

    for key, value in body.items():
        text += (
            indent * w
            + bold(key)
            + ((value[0] + n) if isinstance(value, list) else mono(value))
        )
    return text


regex_upvote = r"^(\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍|\+\+ .+)$"
regex_downvote = r"^(-|--|-1|👎|-- .+)$"


@rose.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_upvote, re.IGNORECASE)
    & ~filters.via_bot
    & ~filters.bot
    & ~filters.edited,
    group=karmapositivegrp,
)
async def upvote(_, message):
    if not await is_karma_on(message.chat.id):
        return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma + 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    else:
        karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f"Increased 1 karma of {user_mention}. \nTotal Points: {karma}"
    )


@rose.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote, re.IGNORECASE)
    & ~filters.via_bot
    & ~filters.bot
    & ~filters.edited,
    group=karmanegativegrp,
)
async def downvote(_, message):
    if not await is_karma_on(message.chat.id):
        return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return

    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma - 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    else:
        karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f"Decreased 1 karma of {user_mention}\nTotal Points: {karma}"
    )


@rose.on_message(filters.command("karma") & filters.group)
async def command_karma(_, message):
  chat_id = message.chat.id
  user = await message.chat.get_member(message.from_user.id)
  admin_strings = ("creator", "administrator") 
  if len(message.command) == 2 and (user.status in admin_strings or user in DRAGONS):
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "on":
        await karma_on(chat_id)
        return await message.reply_text("Karma turned on.")
    elif state == "off":
        await karma_off(chat_id)
        return await message.reply_text("Karma turned off.")  
  else: 
    if not message.reply_to_message:
        m = await message.reply_text("Loading Karma...")
        karma = await get_karmas(chat_id)
        if not karma:
            return await m.edit("No karma in DB for this chat.")
        msg = f"Karma list of {message.chat.title}"
        limit = 0
        karma_dicc = {}
        for i in karma:
            user_id = await alpha_to_int(i)
            user_karma = karma[i]["karma"]
            karma_dicc[str(user_id)] = user_karma
            karma_arranged = dict(
                sorted(
                    karma_dicc.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
        if not karma_dicc:
            return await m.edit("No karma in DB for this chat.")
        userdb = await get_user_id_and_usernames(rose)
        karma = {}
        for user_idd, karma_count in karma_arranged.items():
            if limit > 15:
                break
            if int(user_idd) not in list(userdb.keys()):
                continue
            username = userdb[int(user_idd)]
            karma["@" + username] = ["**" + str(karma_count) + "**"]
            limit += 1
        await m.edit(section(msg, karma))
    else:
        if not message.reply_to_message.from_user:
            return await message.reply("Anon user has no karma.")

        user_id = message.reply_to_message.from_user.id
        karma = await get_karma(chat_id, await int_to_alpha(user_id))
        if karma:
            karma = karma["karma"]
            await message.reply_text(f"**Total Points**: __{karma}__")
        else:
            karma = 0
            await message.reply_text(f"**Total Points**: __{karma}__")

__help__ = """
❍ /karma `[on/off]` - On and off Karma.
❍ /karma - Check karma stats.
❍ /karma `[reply user]` - Check karma of replied user.
"""
__mod_name__ = "Karma🔱"
