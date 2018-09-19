import discord
from discord.ext import commands

import face_recognition
from PIL import Image, ImageDraw

from .utils.chat_formatting import escape_mass_mentions, italics, pagify
from random import randint
from random import choice
from enum import Enum
from urllib.parse import quote_plus
from pathlib import Path
import urllib.request
import datetime
import time
import aiohttp
import asyncio
import uuid
import os, random
from os import listdir
from os.path import isfile, join
import itertools 
from random import shuffle

class Bts:
    """My custom cog that does stuff!"""

    def check_folders(self):
        # DELETE STUFF IN HERE if u want to clear the cache cause i'm not doing it for u
        folders = ("/data/bts/", "/data/bts/imageCache/", "/data/bts/pics/", "/data/bts/creations/")

        for folder in folders:
            if not os.path.exists(folder):
                print("Creating " + folder + " folder...")
                os.makedirs(folder)

    def __init__(self, bot):
        self.check_folders()
        self.bot = bot

    @commands.command(no_pm=True)
    async def btsSaveNewImage(self, imageUrl):
        """ do "[btsSaveNewImage] [imageUrl]" to save a new image to the DB """
        try:
            imagePath = "/data/bts/pics/" + str(uuid.uuid1())
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(imageUrl, imagePath)
            print("Saving image: " + imagePath)
        except:
            await self.bot.say("u broke me :C")


    @commands.command(pass_context=True, no_pm=True)
    async def pics(self, ctx, *users : discord.Member):
        """Because everyone loves bts. Do "$pics [user] [user2] ..." and see what happens """
        for user in users:
            # Get the avatar and cache it
            imagePath = "/data/bts/imageCache/" + user.id + ".png"
            if not Path(imagePath).is_file():
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve("https://cdn.discordapp.com/avatars/" + user.id + "/" + user.avatar + ".png", imagePath)
                print("Caching image: " + imagePath)

        # check if any files exist
        randomBts = random.choice(os.listdir("/data/bts/pics/"))
        if randomBts:
            btsImage = face_recognition.load_image_file("/data/bts/pics/" + randomBts)
            face_locations = face_recognition.face_locations(btsImage)

            # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
            # See http://pillow.readthedocs.io/ for more about PIL/Pillow
            pil_image_bts = Image.fromarray(btsImage)
            # Create a Pillow ImageDraw Draw instance to draw with
            draw_bts = ImageDraw.Draw(pil_image_bts)

            shuffle(face_locations)
            for (top, right, bottom, left), user in zip(face_locations, users):
                avatar = Image.open("/data/bts/imageCache/" + user.id + ".png")
                avatar = avatar.resize((right-left, bottom-top), Image.LANCZOS)
                pil_image_bts.paste(avatar, (left, top))

            newImageId = "data/bts/creations" + str(uuid.uuid1()) + ".png"
            pil_image_bts.save(newImageId)

            await self.bot.send_file(ctx.message.channel, newImageId)
            del draw_bts

def setup(bot):
    bot.add_cog(Bts(bot))