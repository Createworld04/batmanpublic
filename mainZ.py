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
import pycurl

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
    editable = await m.reply_text("Hello im txt file downloader\nPress /pyro to download links listed in a txt file in the format **Name:link**\n\nPress /link to download single link\nPress /ytdlp to know video info.\nPress /aio to download url.\n\nBot made by ACE")
#testing topranker
# @bot.on_message(filters.command(["top"])& ~filters.edited)
# async def upload(bot: Client, m: Message):
    
#     getstatusoutput(f'curl "https://onlinetest.sure60.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fvodcdn.sure60.com%2Flivehttporigin%2F3525433%2F3525433-pr-class-10--10000-1632493792901%2Fmaster.m3u8" -c "cookie.txt"')
#     y = "cookie.txt"  
#     await m.reply_document(y)
#     cmd = f'yt-dlp -o "top.mp4" --cookies cookie.txt "https://vodcdn.sure60.com/livehttporigin/3525433/3525433-pr-class-10--10000-1632493792901/master.m3u8"'
#     download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
#     os.system(download_cmd)
#     await m.reply_video("top.mp4",supports_streaming=True,height=720,width=1280 )
#     os.remove(y)
#     os.remove("top.mp4")
        
@bot.on_message(filters.command(["link"])& ~filters.edited)
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('Send link in **Name&link** format to download')
    input9: Message = await bot.listen(editable.chat.id)
    raw = input9.text    
    name = raw.split('&')[0]
    url = raw.split('&')[1] or raw
    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    
    Show = f"**Downloading:-**\n\n**Name :-** ```{name}\nQuality - {raw_text2}```\n\n**Url :-** ```{url}```"
    prog = await m.reply_text(Show)
    
    cc = f'>> **Name :** {name}'
    
    
    if "youtu" in url:
        if raw_text2 in ["144", "240", "480"]:
            ytf = f'bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]'
        elif raw_text2 == "360":
            ytf = "18/134"
        elif raw_text2 == "720":
            ytf = "22/136/18"
        elif raw_text2 =="1080":
            ytf = "137/399"
        else:
            ytf = 18
    else:
        ytf=f"bestvideo[height<={raw_text2}]"

    if "jwplayer" in url:
        if raw_text2 in ["180", "144"]:
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf = f"{out['320x180 ']}/{out['256x144 ']}"
            except Exception as e:
                if e==0:
                    raw_text2=="no"
        elif raw_text2 in ["240", "270"]:
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf = f"{out['480x270 ']}/{out['426x240 ']}"
            except Exception as e:
                if e==0:
                    raw_text2=="no"
        elif raw_text2 == "360":
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf = out['640x360 ']
            except Exception as e:
                if e == 0:
                    raw_text2=="no"
                #cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
        elif raw_text2 == "480":
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf = f"{out['960x540 ']}/{out['852x480 ']}"
            except Exception as e:
                if e==0:
                    raw_text2=="no"
            # cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
        elif raw_text2 == "720":
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf = f"{out['1280x720 ']}"
            except Exception as e:
                if e==0:
                    raw_text2=="no"
            # cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
        elif raw_text2 == "1080":
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf =f"{out['1920x1080 ']}/{['1920x1056']}"
            except Exception as e:
                if e==0:
                    raw_text2=="no"
        else:
            # cmd = f'yt-dlp -F "{url}"'
            # k = await helper.run(cmd)
            #out = helper.vid_info(str(k))
            # ytf = out['640x360 ']
            #cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
            raw_text2=="no"
#             except Exception as e:
#                 print(e)

    if ytf == f'bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]':
        cmd = f'yt-dlp -o "{name}.mp4" -f "{ytf}" "{url}"'

    # elif "jwplayer" in url:# and raw_text2 in ["144", "240", "360", "480", "720", "no"]:
    #     cmd=f'yt-dlp -o "{name}.mp4" "{url}"'    
    elif "adda247" in url:# and raw_text2 in ["144", "240", "360", "480", "720", "no"]:
        cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
    elif "kdcampus" or "streamlock" in url:
        cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
    elif ".pdf" in url: #and raw_text2 in ["144", "240", "360", "480", "720", "no"]:
        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
    elif "drive" in url:
        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
    elif raw_text2 == "no":# and raw_text2 in ["144", "240", "360", "480", "720", "no"]:
        cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
#             elif "unknown" in ytf:
#                 cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
    else:
        cmd = f'yt-dlp -o "{name}.mp4" -f "{ytf}+bestaudio" "{url}"'

    try:
        download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
        os.system(download_cmd)
        filename = f"{name}.mp4"
        subprocess.run(f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"', shell=True)
        thumbnail = f"{filename}.jpg"
        dur = int(helper.duration(filename))
        await prog.delete (True)
        try:
            await m.reply_video(f"{name}.mp4",caption=cc, supports_streaming=True,height=720,width=1280,thumb=thumbnail,duration=dur)

        except:
            await m.reply_text("There was an error while uploading file as streamable so, now trying to upload as document.")
            await m.reply_document(f"{name}.webm",caption=cc)
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
#             try:
            if "jwplayer" in url:
                if raw_text2 in ["180", "144"]:
                    try:
                        cmd = f'yt-dlp -F "{url}"'
                        k = await helper.run(cmd)
                        out = helper.vid_info(str(k))
                        ytf = f"{out['320x180 ']}/{out['256x144 ']}"
                    except Exception as e:
                        if e==0:
                            raw_text2=="no"
                elif raw_text2 in ["240", "270"]:
                    try:
                        cmd = f'yt-dlp -F "{url}"'
                        k = await helper.run(cmd)
                        out = helper.vid_info(str(k))
                        ytf = f"{out['480x270 ']}/{out['426x240 ']}"
                    except Exception as e:
                        if e==0:
                            raw_text=="no"
                elif raw_text2 == "360":
                    try:
                        cmd = f'yt-dlp -F "{url}"'
                        k = await helper.run(cmd)
                        out = helper.vid_info(str(k))
                        ytf = out['640x360 ']
                    except Exception as e:
                        if e == 0:
                            raw_text2=="no"
                        #cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
                elif raw_text2 == "480":
                    try:
                        cmd = f'yt-dlp -F "{url}"'
                        k = await helper.run(cmd)
                        out = helper.vid_info(str(k))
                        ytf = f"{out['960x540 ']}/{out['852x480 ']}"
                    except Exception as e:
                        if e==0:
                            raw_text2=="no"
                    # cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
                elif raw_text2 == "720":
                    try:
                        cmd = f'yt-dlp -F "{url}"'
                        k = await helper.run(cmd)
                        out = helper.vid_info(str(k))
                        ytf = f"{out['1280x720 ']}"
                    except Exception as e:
                        if e==0:
                            raw_text2=="no"
                    # cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
                elif raw_text2 == "1080":
                    try:
                        cmd = f'yt-dlp -F "{url}"'
                        k = await helper.run(cmd)
                        out = helper.vid_info(str(k))
                        ytf =f"{out['1920x1080 ']}/{['1920x1056']}"
                    except Exception as e:
                        if e==0:
                            raw_text2=="no"
                else:
                   # cmd = f'yt-dlp -F "{url}"'
                   # k = await helper.run(cmd)
                    #out = helper.vid_info(str(k))
                   # ytf = out['640x360 ']
                    #cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
                    raw_text2=="no"
#             except Exception as e:
#                 print(e)
            

            if ytf == f'bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]':
                cmd = f'yt-dlp -o "{name}.mp4" -f "{ytf}" "{url}"'

            # elif "jwplayer" in url:# and raw_text2 in ["144", "240", "360", "480", "720", "no"]:
            #     cmd=f'yt-dlp -o "{name}.mp4" "{url}"'    
            elif "adda247" in url:# and raw_text2 in ["144", "240", "360", "480", "720", "no"]:
                cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
            elif "kdcampus" or "streamlock" in url:
                cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
            elif ".pdf" in url: #and raw_text2 in ["144", "240", "360", "480", "720", "no"]:
                cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
            elif "drive" in url:
                cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
            elif raw_text2 == "no":# and raw_text2 in ["144", "240", "360", "480", "720", "no"]:
                cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
#             elif "unknown" in ytf:
#                 cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -o "{name}.mp4" -f "{ytf}+bestaudio" "{url}"'

            
            
                # download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                # os.system(download_cmd)
            try:
                if cmd == f'yt-dlp -o "{name}.pdf" "{url}"' or "drive" in url:
#                 if "drive" in url:
                    try:
                        ka=await helper.download(url)
                        await prog.delete (True)
                        time.sleep(1)
                        reply = await m.reply_text(f"Uploading - ```{name}```")
                        time.sleep(1)
                        start_time = time.time()
                        await m.reply_document(ka, caption=f'>> **File :** {name}\n>> **Title :** {raw_text0}\n\n>> **Index :** {count}')
                        count+=1
                        # time.sleep(1)
                        await reply.delete (True)
                        time.sleep(1)
                        os.remove(ka)
                        time.sleep(3)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                elif ".pdf" in url:

#                         os.remove(ka)
                    try:
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                        os.system(download_cmd)
                        filename = f"{name}.pdf"
                        await m.reply_document(f'{name}.pdf',caption =f'>> **File :** {name}\n>> **Title :** {raw_text0}\n\n>> **Index :** {count}')
                        count+=1
                        await prog.delete (True)
                        os.remove(f'{name}.pdf')
                        time.sleep(2)
                    except Exception as e:
                        await m.reply_text(f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - ```{url}```")
                        continue
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
