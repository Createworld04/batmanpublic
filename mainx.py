import requests
import json
import subprocess
from pyrogram import Client, client,  filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters
# from details import api_id, api_hash, bot_token
# from dotenv import load_dotenv
import tgcrypto
from p_bar import progress_bar
from subprocess import getstatusoutput
import helper
import logging
import time
import aiohttp
import asyncio
import aiofiles
from pyrogram.types import User, Message
import os

import requests

# bot = Client(
#     "bot",
#     api_id=api_id,
#     api_hash=api_hash,
#     bot_token=bot_token)

bot = Client(
    "bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

logger = logging.getLogger()

os.makedirs("./downloads", exist_ok=True)

@bot.on_message(filters.command(["start"])& ~filters.edited)
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Hello im txt file downloader\nPress /pyro to download links listed in a txt file in the format **Name:link**\n\nPress /ytdlp to know video info.\nPress /aio to download url.\n\nBot made by ACE")
    
@bot.on_message(filters.command(["link"])& ~filters.edited)
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('Send link in **Name&link** format to download')
    input9: Message = await bot.listen(editable.chat.id)
    raw = input9.text    
    name = raw.split('&')[0]
    url = raw.split('&')[1]
    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    
    Show = f"**Downloading:-**\n\n**Name :-** ```{name}\nQuality - {raw_text2}```\n\n**Url :-** ```{url}```"
    prog = await m.reply_text(Show)
    
    if "jwplayer" in url:
        if raw_text2 == "180":
            ytf="190/220/210/200"
        elif raw_text2 == "240":
            ytf="230/240/290/270/250"
        elif raw_text2 == "360":
            ytf="250/280/320/360/300/280/310"
        elif raw_text2 == "480":
            ytf="400/340/390/440/380/490/450"
        elif raw_text2 == "720":
            ytf="540/580/430/500/510/520/600/620/680"
        else:
            raw_text2=="no"
    if "youtu" in url:
        if raw_text2 in ["144", "240", "480"]:
            ytf = f'bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]'
        elif raw_text2 == "360":
            ytf = 18
        elif raw_text2 == "720":
            ytf = "22/18"
        else:
            ytf = 18
    else:
        ytf=f"bestvideo[height<={raw_text2}]"
    if ytf == f'bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]':
        cmd = f'yt-dlp -o "{name}.mp4" -f "{ytf}" "{url}"'
    elif raw_text2 == "no":    
        cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
    elif "adda" in url:
        cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
    else:
        cmd = f'yt-dlp -o "{name}.mp4" -f "{ytf}+bestaudio" "{url}"'
#     cmd = f'yt-dlp -o "{name}.mp4" -f "{ytf}+bestaudio" "{url}"'
    try:
        download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
        os.system(download_cmd)
        filename = f"{name}.mp4"
        subprocess.run(f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"', shell=True)
        thumbnail = f"{filename}.jpg"
        dur = int(helper.duration(filename))
        await prog.delete (True)
        await m.reply_video(f"{name}.mp4",caption=name, supports_streaming=True,height=720,width=1280,thumb=thumbnail,duration=dur)
        os.remove(f"{name}.mp4")
        os.remove(f"{filename}.jpg")
    except Exception as e:
        await m.reply_text(e)
        
    
    
@bot.on_message(filters.command(["aio"])& ~filters.edited)
async def aiohttp(bot: Client, m: Message):
    editable = await m.reply_text('Send link in **Name&link** format to download')
    input9: Message = await bot.listen(editable.chat.id)
    raw = input9.text    
    name = raw.split('&')[0]
    url = raw.split('&')[1]
    p =await m.reply_text("Downloading")
    k = await helper.aio(url)
    await m.reply_document(k, caption=name)
    await p.delete(True)
    os.remove(k)
    
@bot.on_message(filters.command(["ytdlp"])& ~filters.edited)
async def account_login(bot: Client, m: Message):
    
    editable = await m.reply_text('Send link in **Name&link** format to get its info')
    input: Message = await bot.listen(editable.chat.id)
    raw_file = input.text    
    name = raw_file.split('&')[0]
    url = raw_file.split('&')[1]   
    cmd = f'yt-dlp -F "{url}"'
    k = await helper.run(cmd)
    out = helper.parse_vid_info(str(k))
    await m.reply_text(out)
    buttons = []
    if 'unknown' in out[0][1]:
        r = await m.reply_text("Its Unknown so Downloading")
        f = helper.old_download(url, name)
#         res_file = await fast_upload(bot, f, r)
        await m.reply_document(
        document=f,caption=name
        )
        await r.delete(True)
        return
    
    for i in out:
        if 'youtu' in url:
            await m.reply_text(i[1])
            x = i[1].split()[0].split("x")[-1]
            buttons.append(InlineKeyboardButton(i[1], callback_data=f"id:bestvideo[height<={x}][ext=mp4]"))
        else:
            buttons.append(InlineKeyboardButton(i[1], callback_data=f"id:{i[0]}"))
    buttons_markup = InlineKeyboardMarkup([buttons])
    await m.reply(f"Name : `{name}`\n\n:Link : `{url}`",reply_markup=buttons_markup)
            
        
        
# @bot.on_message(filters.command(["link"])& ~filters.edited)
# async def account_login(bot: Client, m: Message):
#     editable = await m.reply_text('Send **Name&link** to download')

#     input: Message = await bot.listen(editable.chat.id)
#     raw_file = input.text

#     name = raw_file.split('&')[0]
#     url = raw_file.split('&')[1]


@bot.on_message(filters.command(["pyro"])& ~filters.edited)
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Send txt file**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    # editable = await m.reply_text("**Send From where you want to download**")
    # input1: Message = await bot.listen(editable.chat.id)
    # raw_text = input1.text

    

    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await m.reply_text(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text)
    except:
        arg = 0
    
    
    editable = await m.reply_text("Enter Title")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text0 = input0.text
    
    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

    editable4= await m.reply_text("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/d9e24878bd4aba05049a1.jpg```\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"
        
           
    count =int(raw_text)    
    try:
        for i in range(arg, len(links)):
        
            url = links[i][1]
            name = links[i][0].replace("\t", "")
                # await m.reply_text(name +":"+ url)

            Show = f"**Downloading:-**\n\n**Name :-** ```{name}\nQuality - {raw_text2}```\n\n**Url :-** ```{url}```"
            prog = await m.reply_text(Show)
            cc = f'>> **Name :** {name}\n>> **Title :** {raw_text0}\n\n>> **Index :** {count}'

            if "youtu" in url:
                if raw_text2 in ["144", "240", "480"]:
                    ytf = f'bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]'
                elif raw_text2 == "360":
                    ytf = 18
                elif raw_text2 == "720":
                    ytf = "22/18"
                else:
                    ytf = 18
            else:
                ytf=f"bestvideo[height<={raw_text2}]"

            if ytf == f'bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]':
                cmd = f'yt-dlp -o "{name}.mp4" -f "{ytf}" "{url}"'
            elif raw_text2 == "no":
                cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
            elif "jwplayer" in url:# and raw_text2 in ["144", "240", "360", "480", "720", "no"]:
                cmd=f'yt-dlp -o "{name}.mp4" "{url}"'    
            elif "adda" in url:# and raw_text2 in ["144", "240", "360", "480", "720", "no"]:
                cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
            elif ".pdf" in url: #and raw_text2 in ["144", "240", "360", "480", "720", "no"]:
                cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
            elif "drive" in url:
                cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
            else:
                cmd = f'yt-dlp -o "{name}.mp4" -f "{ytf}+bestaudio" "{url}"'

            
                # download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                # os.system(download_cmd)
            try:
                if cmd == f'yt-dlp -o "{name}.pdf" "{url}"' or ".pdf" in url:
                    try:
                        ka=await helper.download(url)
                        await prog.delete (True)
                        time.sleep(1)
                        reply = await m.reply_text(f"Uploading - ```{name}```")
                        time.sleep(1)
                        start_time = time.time()
                        await m.reply_document(ka, caption=f'>> **File :** {name}\n>> **Title :** {raw_text0}\n\n>> **Index :** {count}')
                        count+=1
                        time.sleep(1)
                        await reply.delete (True)
                        time.sleep(1)
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                        
#                         os.remove(ka)

                    # filename = f"{name}.pdf"
                    # await m.reply_document(f'{name}.pdf',caption =f'>> **File :** {name}\n>> **Title :** {raw_text0}\n\n>> **Index :** {count}', progress=progress_bar,progress_args=(reply,start_time))
                    # count+=1
                    # await prog.delete (True)
                    # os.remove(f'{name}.pdf')
#                        time.sleep(2)
                else:
                    try:
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                        os.system(download_cmd)
                        filename = f"{name}.mp4"
                        subprocess.run(f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"', shell=True)
                        await prog.delete (True)
                        reply = await m.reply_text(f"Uploading - ```{name}```")
                        try:
                            if thumb == "no":
                                thumbnail = f"{filename}.jpg"
                            else:
                                thumbnail = thumb
                        except Exception as e:
                            await m.reply_text(str(e))

                        dur = int(helper.duration(filename))
            #                         await prog.delete (True)
                        start_time = time.time()
                        await m.reply_video(f"{name}.mp4",caption=cc, supports_streaming=True,height=720,width=1280,thumb=thumbnail,duration=dur, progress=progress_bar,progress_args=(reply,start_time))
                        count+=1
                        os.remove(f"{name}.mp4")

                        os.remove(f"{filename}.jpg")
                        await reply.delete (True)
                        time.sleep(1)
                    except Exception as e:
                        await m.reply_text(f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - ```{url}```")
                        continue
            except Exception as e:
                await m.reply_text(str(e))
                continue
    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done")





    # except Exception as e:
    #     await m.reply_text(str(e))
    # await m.reply_text("Done sleeping for 10 sec")
    # time.sleep(10)










bot.run()
