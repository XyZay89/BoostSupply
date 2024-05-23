from discord.ext import commands
import discord
import requests
from time import sleep
import uuid
import random
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

gift_links = [
    "https://discord.gift/QCZnbtEKy4JHSpmpfnWx2Z4f",
    "https://discord.gift/eC969wN9wHfnfSSxDAShM3U4",
    "https://discord.gift/dM76Tj7NSfqN64kVpn9JBJdE"
]

@bot.event
async def on_ready():
    print("Bot is online and ready")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 
    
    if isinstance(message.channel, discord.DMChannel):
        await bot.process_commands(message)

@bot.command()
async def add_keys(ctx, amount):
    user_id = str(ctx.author.id)
    with open("admin.txt", "r") as f:
        if user_id in f.read():
            key_amt = range(int(amount))
            f = open("keys.txt", "a")
            show_key = ''
            for x in key_amt:
                key = str(uuid.uuid4())
                show_key += "\n" + key
                f.write(key)
                f.write("\n")

            if len(str(show_key)) == 37:
                show_key = show_key.replace('\n', '')
                em = discord.Embed(color=0x00ff00)
                em.add_field(name="__[BoostSupply] Successfully Generated Key(s)__", value=f"```{show_key}```")
                await ctx.author.send(embed=em)
                return 0
            if len(str(show_key)) > 37:
                em = discord.Embed(color=0x00ff00)
                em.add_field(name="__[BoostSupply] Successfully Generated Key(s)__", value=f"```{show_key}```")
                await ctx.author.send(embed=em)
            else:
                em = discord.Embed(color=0xff0000)
                em.add_field(name="__[BoostSupply] API Error__", value="Something's wrong !")
                await ctx.author.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
            await ctx.author.send(embed=em)

        

@bot.command()
async def gen_nitro(ctx, key):
    user_id = str(ctx.author.id)
    with open("blacklisted.txt", "r") as f:
        if user_id in f.read():
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You have been banned !")
            await ctx.author.send(embed=em)
            return False

    if len(key) == 36:
        with open("used keys.txt") as f:
            if key in f.read():
                em = discord.Embed(color=0xff0000)
                em.add_field(name="__[BoostSupply] Key Already Redeemed__", value="Inputed key has already been used !")
                await ctx.author.send(embed=em)
                return 0

        with open("keys.txt") as f:
            if key in f.read():
                em = discord.Embed(color=0x00ff00)
                em.add_field(name="__[BoostSupply] x1 Month Nitro Boost Generated__", value=f"")
                await ctx.author.send(embed=em)
                random_gift = random.choice(gift_links)
                await ctx.author.send(random_gift)

                f = open("used keys.txt", "a")
                f.write(key)
                f.write('\n')

                with open("logs.txt", "a") as f:
                    f.write(f"[{datetime.now()}] - [User: {ctx.author.id} ({ctx.author.name})] - [Key: {key}] - [Nitro Code: {random_gift}]\n")
            else:
                em = discord.Embed(color=0xff0000)
                em.add_field(name="__[BoostSupply] Key Invalid__", value="Inputed key is invalid !")
                await ctx.author.send(embed=em)
    else:
        em = discord.Embed(color=0xff0000)
        em.add_field(name="__[BoostSupply] Key Invalid__", value="Inputed key is invalid !")
        await ctx.author.send(embed=em)


@bot.command()
async def show_keys(ctx):
    user_id = str(ctx.author.id)
    with open("admin.txt", "r") as f_admin:
        if user_id in f_admin.read():
            try:
                with open("keys.txt", "r") as f_keys:
                    keys_content = f_keys.read()
                    em = discord.Embed(color=0x00ff00)
                    em.add_field(name="__[BoostSupply] List Of All Key(s)__", value=f"```{keys_content}```")
                    await ctx.author.send(embed=em)
            except FileNotFoundError:
                em = discord.Embed(color=0xff0000)
                em.add_field(name="__[BoostSupply] API Error__", value="Key(s) not found !")
                await ctx.author.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
            await ctx.author.send(embed=em)

@bot.command()
async def delete_key(ctx, key: str):
    user_id = str(ctx.author.id)
    with open("admin.txt", "r") as f:
        if user_id in f.read():
            with open("keys.txt", "r") as f:
                keys = f.readlines()
                
            if key + '\n' in keys:
                keys.remove(key + '\n')
                with open("keys.txt", "w") as f:
                    f.writelines(keys)
                em = discord.Embed(color=0x00ff00)
                em.add_field(name="__[BoostSupply] Successfully Deleted Key__", value=f"The key `{key}` has been deleted !")
                await ctx.author.send(embed=em)
            else:
                em = discord.Embed(color=0xff0000)
                em.add_field(name="__[BoostSupply] Key Error__", value=f"The key `{key}` does not exist !")
                await ctx.author.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command!")
            await ctx.author.send(embed=em)

@bot.command()
async def delete_all_keys(ctx):
    user_id = str(ctx.author.id)
    with open("admin.txt", "r") as f:
        if user_id in f.read():
            with open("keys.txt", "w") as f:
                f.write("")
            em = discord.Embed(color=0x00ff00)
            em.add_field(name="__[BoostSupply] Successfully All Deleted Key(s)__", value="All key(s) have been deleted !")
            await ctx.author.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
            await ctx.author.send(embed=em)

@bot.command()
async def delete_used_key(ctx, key: str):
    user_id = str(ctx.author.id)
    with open("admin.txt", "r") as f:
        if user_id in f.read():
            with open("used keys.txt", "r") as f:
                keys = f.readlines()
                
            if key + '\n' in keys:
                keys.remove(key + '\n')
                with open("used keys.txt", "w") as f:
                    f.writelines(keys)
                em = discord.Embed(color=0x00ff00)
                em.add_field(name="__[BoostSupply] Successfully Deleted Used Key__", value=f"The key `{key}` has been deleted !")
                await ctx.author.send(embed=em)
            else:
                em = discord.Embed(color=0xff0000)
                em.add_field(name="__[BoostSupply] Key Error__", value=f"The key `{key}` does not exist !")
                await ctx.author.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command!")
            await ctx.author.send(embed=em)

@bot.command()
async def delete_all_used_keys(ctx):
    user_id = str(ctx.author.id)
    with open("admin.txt", "r") as f:
        if user_id in f.read():
            with open("used keys.txt", "w") as f:
                f.write("")

                em = discord.Embed(color=0x00ff00)
                em.add_field(name="__[BoostSupply] Successfully Deleted Used Key(s)__", value="All used key(s) have been deleted !")
                await ctx.author.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
            await ctx.author.send(embed=em)

@bot.command()
async def show_used_keys(ctx):
    user_id = str(ctx.author.id)
    with open("admin.txt", "r") as f:
        if user_id in f.read():
            try:
                with open("used keys.txt", "r") as f:
                    keys_unused_content = f.read()
                    em = discord.Embed(color=0x00ff00)
                    em.add_field(name="__[BoostSupply] List Of All Used Key(s)__", value=f"```{keys_unused_content}```")
                    await ctx.author.send(embed=em)
            except FileNotFoundError:
                    em = discord.Embed(color=0xff0000)
                    em.add_field(name="__[BoostSupply] API Error__", value="Key(s) not found !")
                    await ctx.author.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
            await ctx.author.send(embed=em)

@bot.command()
async def ban(ctx, user_id):
    admin_id = str(ctx.author.id)
    with open("admin.txt", "r") as f_admin:
        if admin_id in f_admin.read():
            with open("blacklisted.txt", "a") as f_blacklisted:
                f_blacklisted.write(user_id + "\n")
            em = discord.Embed(color=0x00ff00)
            em.add_field(name="__[BoostSupply] User Banned__", value=f"User with ID `{user_id}` has been banned !")
            await ctx.author.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
            await ctx.author.send(embed=em)

@bot.command()
async def show_ban(ctx):
    user_id = str(ctx.author.id)
    with open("admin.txt", "r") as f_admin:
        if user_id in f_admin.read():
            try:
                with open("blacklisted.txt", "r") as f_blacklisted:
                    keys_unused_content = f_blacklisted.read()
                    em = discord.Embed(color=0x00ff00)
                    em.add_field(name="__[BoostSupply] List Of All User(s) Banned__", value=f"```{keys_unused_content}```")
                    await ctx.author.send(embed=em)
            except FileNotFoundError:
                em = discord.Embed(color=0xff0000)
                em.add_field(name="__[BoostSupply] API Error__", value="User(s) not found !")
                await ctx.author.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
            await ctx.author.send(embed=em)

@bot.command()
async def unban(ctx, user_id):
    admin_id = str(ctx.author.id)
    with open("admin.txt", "r") as f_admin:
        if admin_id in f_admin.read():
            with open("blacklisted.txt", "r") as f_blacklisted:
                lines = f_blacklisted.readlines()

            found = False
            with open("blacklisted.txt", "w") as f:
                for line in lines:
                    if line.strip() != user_id:
                        f.write(line)
                    else:
                        found = True

            if found:
                em = discord.Embed(color=0x00ff00)
                em.add_field(name="__[BoostSupply] User Unbanned__", value=f"User with ID `{user_id}` has been unbanned !")
                await ctx.author.send(embed=em)
            else:
                em = discord.Embed(color=0xff0000)
                em.add_field(name="__[BoostSupply] ID Not Banned__", value="This ID is not banned !")
                await ctx.author.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
            await ctx.author.send(embed=em)

@bot.command()
async def add_admin(ctx, user_id):
    if ctx.author.id != 1220399982331428864:
        em = discord.Embed(color=0xff0000)
        em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
        await ctx.author.send(embed=em)
        return
    
    with open("admin.txt", "a") as f:
        f.write(user_id + "\n")
    
    em = discord.Embed(color=0x00ff00)
    em.add_field(name="__[BoostSupply] New Admin__", value=f"User with ID `{user_id}` is admin !")
    await ctx.author.send(embed=em)

@bot.command()
async def show_admin(ctx):
    if ctx.author.id != 1220399982331428864:
        em = discord.Embed(color=0xff0000)
        em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
        await ctx.author.send(embed=em)
        return
    try:
        with open("admin.txt", "r") as f:
            admin_content = f.read()
            em = discord.Embed(color=0x00ff00)
            em.add_field(name="__[BoostSupply] List Of All Admin(s)__", value=f"{admin_content}")
            await ctx.author.send(embed=em)
    except FileNotFoundError:
        em = discord.Embed(color=0xff0000)
        em.add_field(name="__[BoostSupply] API Error__", value="Admin(s) not found !")
        await ctx.author.send(embed=em)

@bot.command()
async def delete_admin(ctx, user_id):
    if ctx.author.id != 1220399982331428864:
        em = discord.Embed(color=0xff0000)
        em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
        await ctx.author.send(embed=em)
        return
    
    with open("admin.txt", "r") as f:
        lines = f.readlines()
    
    found = False
    with open("admin.txt", "w") as f:
        for line in lines:
            if line.strip() != user_id:
                f.write(line)
            else:
                found = True
    
    if found:
        em = discord.Embed(color=0x00ff00)
        em.add_field(name="__[BoostSupply] Admin Deleted__", value=f"User with ID `{user_id}` is no longer admin !")
        await ctx.author.send(embed=em)
    else:
        em = discord.Embed(color=0xff0000)
        em.add_field(name="__[BoostSupply] User Not Admin__", value="This user is not admin !")
        await ctx.author.send(embed=em)

@bot.command(name='delete_msg')
async def delete_msg(ctx):
    admin_id = str(ctx.author.id)
    with open("admin.txt", "r") as f_admin:
        if admin_id in f_admin.read():
            deleted = 0
            async for msg in ctx.author.history(limit=100):
                if msg.author == bot.user:
                    await msg.delete()
                    deleted += 1
                    if deleted % 2 == 0:
                        await discord.utils.sleep_until(asyncio.get_event_loop().time() + 3)
                    if deleted >= 10:
                        break
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="__[BoostSupply] API Error__", value="You are not authorized to execute this command !")
            await ctx.author.send(embed=em)

bot.run('MTI0MjU2MzQ3ODU0NDQ1Mzc1NQ.GXYuKU.SUSrs8qX51FxvOa2xdklwArgdl6cqXuMTSmuwI')
