# Powered By #Adi

import os
import re
import textwrap
import random
import aiofiles
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch

from config import MUSIC_BOT_NAME, YOUTUBE_IMG_URL
from back import files

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}_{anime}.png"):
        return f"cache/{videoid}_{anime}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(
                        f"cache/thumb{videoid}.png", mode="wb"
                    )
                    await f.write(await resp.read())
                    await f.close()

        image1 = Image.open(f"cache/thumb{videoid}.png")
        image2 = Image.open(f"back/{anime}.png")
        image3 = changeImageSize(1280, 720, image1)
        image4 = changeImageSize(1280, 720, image2)
        image5 = image3.convert("RGBA")
        image6 = image4.convert("RGBA")
        Image.alpha_composite(image5, image6).save("cache/temp.png")
        logo = Image.open("cache/temp.png")
        img = ImageOps.expand(logo, border=10, fill=f"{border}")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("assets/font.ttf", 32)
        draw.text((190, 555), f"Title: {title[:50]} ...", (255, 255, 255), font=font)
        draw.text((190, 595), f"Duration: {duration}", (255, 255, 255), font=font)
        draw.text((190, 635), f"Views: {views}", (255, 255, 255), font=font)
        draw.text((190, 675), f"Oreki", (255, 255, 255), font=font)
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/q{videoid}_{anime}.png")
        return f"cache/q{videoid}_{anime}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
