import time
from userbot import *
from TgxBot.utils import *
from userbot.cmdhelp import CmdHelp
from telethon import events, version
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon import version
from userbot import ALIVE_NAME, StartTime, Tgxversion
from TgxBot.utils import admin_cmd, edit_or_reply, sudo_cmd


#-------------------------------------------------------------------------------


async def reply_id(event):
    reply_to_id = None
    if event.sender_id in Config.SUDO_USERS:
        reply_to_id = event.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    return reply_to_id

ludosudo = Config.SUDO_USERS
if ludosudo:
    sudou = "True"
else:
    sudou = "False"

DEFAULTUSER = ALIVE_NAME or "Tgx User"
Tgx_IMG = Config.ALIVE_PIC
CUSTOM_ALIVE_TEXT = Config.ALIVE_MSG or "Legendary TgxBot"

USERID = bot.uid

mention = f"[{DEFAULTUSER}](tg://user?id={USERID})"


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


uptime = get_readable_time((time.time() - StartTime))


@bot.on(admin_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    reply_to_id = await reply_id(alive)

    if Tgx_IMG:
        Tgx_caption = f"**{CUSTOM_ALIVE_TEXT}**\n\n"
        Tgx_caption = f"𝚃𝙶𝚇 𝚄𝚜𝚎𝚛𝙱𝚘𝚝 𝚒𝚜 𝙰𝚕𝚒𝚟𝚎!!\n\n"

        Tgx_caption = f"𝚂𝚞𝚙𝚙𝚘𝚛𝚝 𝙶𝚛𝚘𝚞𝚙:- @TGXUserBotSupport\n"
        Tgx_caption = f"𝚄𝚙𝚍𝚊𝚝𝚎𝚜 𝙲𝚑𝚊𝚗𝚗𝚎𝚕:- @TGXUserBot\n"
        Tgx_caption = f"𝙿𝚘𝚠𝚎𝚛𝚎𝚍 𝚋𝚢:- @TheDarkZTech\n\n"
        Tgx_caption = f"**MY MASTER 👉 :** {mention}\n"
        Tgx_caption = f"**UPTIME:-** `{uptime}`\n"

        await alive.client.send_file(
            alive.chat_id, Tgx_IMG, caption=Tgx_caption, reply_to=reply_to_id
        )
    else:
        await edit_or_reply(
            alive,
            f"**{CUSTOM_ALIVE_TEXT}**\n\n"
            f"𝚃𝙶𝚇 𝚄𝚜𝚎𝚛𝙱𝚘𝚝 𝚒𝚜 𝙰𝚕𝚒𝚟𝚎!!\n\n"

            f"𝚂𝚞𝚙𝚙𝚘𝚛𝚝 𝙶𝚛𝚘𝚞𝚙:- @TGXUserBotSupport\n"
            f"𝚄𝚙𝚍𝚊𝚝𝚎𝚜 𝙲𝚑𝚊𝚗𝚗𝚎𝚕:- @TGXUserBot\n"
            f"𝙿𝚘𝚠𝚎𝚛𝚎𝚍 𝚋𝚢:- @TheDarkZTech\n\n"
            f"**MY MASTER 👉 :** {mention}\n"
            f"**UPTIME:-** `{uptime}`\n"

 
CmdHelp("alive").add_command(
  'alive', None, 'Check weather the bot is alive or not'
  ).add_info(
  'ARE YOU ALIVE?'
).add()
