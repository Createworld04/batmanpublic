import requests
import json
import subprocess
from pyrogram import Client, client,  filters
from pyrogram.types.messages_and_media import message
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters
# from details import api_id, api_hash, bot_token
# from dotenv import load_dotenv
import tgcrypto
from pyrogram.errors import FloodWait
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

logging.basicConfig(
    # filename="bot.log",
    format="%(asctime)s:%(levelname)s %(message)s",
    # filemode="w",
    level=logging.WARNING,
)


logger = logging.getLogger()
# class Timer:
#     # Time Interval Between Progress Updates Current is 10sec
#     def __init__(self, time_between=10):
#         self.start_time = time.time()
#         self.time_between = time_between

#     def can_send(self):
#         if time.time() > (self.start_time + self.time_between):
#             self.start_time = time.time()
#             return True
#         return False


# timer = Timer()



timer = Timer()

os.makedirs("./downloads", exist_ok=True)

@bot.on_message(filters.command(["start"])& ~filters.edited)
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Hello im txt file downloader\nPress **/pyro** to download links listed in a txt file in the format **Name:link**\nBot made by ACE")
    
    
    
    
class Timer:
    # Time Interval Between Progress Updates Current is 10sec
    def __init__(self, time_between=10):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

timer = Timer()
    
    
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
        
           
    count =1    
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
                    ytf = 22
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
                    ka=await helper.download(url)
                    if timer.can_send():
                        async def progress_bar(current,total):
                            try:
                                await reply.edit(f"{current * 100 / total:.1f}%")
                            except FloodWait as e:
                                time.sleep(e.x)
                    reply = await message.reply("Uploading")
                    start_time = time.time()

                    await m.reply_document(ka, caption=f'>> **File :** {name}\n>> **Title :** {raw_text0}\n\n>> **Index :** {count}',progress=progress_bar,progress_args=(reply,start_time))
                    count+=1
                    await prog.delete (True)
                    os.remove(ka)

                    # filename = f"{name}.pdf"
                    # await m.reply_document(f'{name}.pdf',caption =f'>> **File :** {name}\n>> **Title :** {raw_text0}\n\n>> **Index :** {count}')
                    # count+=1
                    # await prog.delete (True)
                    # os.remove(f'{name}.pdf')
                    # time.sleep(2)
                else:
                    try:
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                        os.system(download_cmd)
                        filename = f"{name}.mp4"
                        subprocess.run(f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"', shell=True)
                        await prog.delete (True)
                        if timer.can_send():
                            async def progress_bar(current,total):
                                try:
                                    await reply.edit(f"{current * 100 / total:.1f}%")
                                except FloodWait as e:
                                    time.sleep(e.x)
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
