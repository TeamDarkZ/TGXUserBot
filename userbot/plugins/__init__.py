from userbot import *
from userbot.Config import Config
from userbot.helpers.functions import *
from userbot.cmdhelp import CmdHelp
from TgxBot.utils import *
from telethon import events, version
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User



# =================== CONSTANT ===================

USERID = bot.uid
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Tgx User"
# mention user
mention = f"[{DEFAULTUSER}](tg://user?id={USERID})"
hmention = f"<a href = tg://user?id={USERID}>{DEFAULTUSER}</a>"