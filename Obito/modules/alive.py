from telethon import events, Button, custom
import re, os
from Obito.events import register
from Obito import telethn as tbot
from Obito import telethn as tgbot
PHOTO = "https://telegra.ph/file/0d239215b8e4382f970ab.mp4"
@register(pattern=("/alive"))
async def awake(event):
 Obito = event.sender.first_name
 Obito = "♡ I,m Obito💕 \n\n"
 Obito += "♡ I'm Working with awesome speed**\n\n"
 Obito += "**♡Obito : 1.0 LATEST**\n\n"
 Obito += "**♡ 𝘔𝘺 𝘰𝘸𝘯𝘦𝘳 : [𝘈𝘴𝘩𝘶👑](t.me/doreamon_music)\n\n"
 Obito += "**♡ Telethon Version : 1.23.0**\n\n"
 BUTTON = [[Button.url("𝘚𝘶𝘱𝘱𝘰𝘳𝘵🔥", "https://t.me/Darkphoenix_Support"), Button.url("𝘜𝘱𝘥𝘢𝘵𝘦𝘴", "https://t.me/Obito_updates")]]
 await tbot.send_file(event.chat_id, PHOTO, caption=Obito,  buttons=BUTTON)
