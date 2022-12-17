from tkinter.tix import INTEGER
import discord
from event import Event
from discord.ext import commands
import sqlite3
import random
import asyncio

client = commands.Bot(command_prefix="?", intents=discord.Intents.all())


@client.event
async def on_ready():
  print("did someone say jojo?")


@client.command(name="kira", description="The kira copypasta")
async def kira(ctx):
    await ctx.send("My name is Yoshikage Kira. I'm 33 years old. My house is in the northeast section of Morioh, where all the villas are, and I am not married. I work as an employee for the Kame Yu department stores, and I get home every day by 8 PM at the latest. I don't smoke, but I occasionally drink. I'm in bed by 11 PM, and make sure I get eight hours of sleep, no matter what. After having a glass of warm milk and doing about twenty minutes of stretches before going to bed, I usually have no problems sleeping until morning. Just like a baby, I wake up without any fatigue or stress in the morning. I was told there were no issues at my last check-up. I'm trying to explain that I'm a person who wishes to live a very quiet life. I take care not to trouble myself with any enemies, like winning and losing, that would cause me to lose sleep at night. That is how I deal with society, and I know that is what brings me happiness. Although, if I were to fight I wouldn't lose to anyone.")

client.add_cog(Event(client))

@client.command()
async def balance(ctx,member:discord.Member=None):
    if member is None:
        member=ctx.author

    db=sqlite3.connect("main.sqlite")
    cursor=db.cursor()

    cursor.execute(f"SELECT wallet,bank FROM main WHERE user_id={member.id}")
    bal=cursor.fetchone()

    try:
        wallet=bal[0]
        bank=bal[1]
    except:
        wallet=0
        bank=0

    embed = discord.Embed(title="Balance",color=0xf1c40f)
    embed.add_field(name="Wallet", value=wallet, inline=False)
    embed.add_field(name="Bank", value=bank, inline=False)
    await ctx.send(embed=embed)

@client.command()
async def beg(ctx):
    member=ctx.author

    earnings=random.randint(0,5)

    db=sqlite3.connect("main.sqlite")
    cursor=db.cursor()

    cursor.execute(f"SELECT wallet FROM main WHERE user_id={member.id}")
    wallet=cursor.fetchone()

    try:
        wallet=wallet[0]
    except:
        wallet=0

    sql=("UPDATE main SET wallet = ? WHERE user_id = ?")
    val = (wallet+int(earnings),member.id)
    cursor.execute(sql,val)

    if earnings==0:
        await ctx.send("You got nothing! Get a job you lazy bum")
    else:
        await ctx.send(f"You got {earnings}!")

    db.commit()
    cursor.close()
    db.close()

@client.command()
async def higherlower(ctx):
    hint=random.randint(1,100)
    number=random.randint(1,100)
    embed = discord.Embed(title="Higher or Lower",description="is the number higher or lower than the hint?",color=0xf1c40f)
    embed.add_field(name="Hint", value=hint, inline=False)
    print(number)
    await ctx.send(embed=embed)
    try:
        message=await client.wait_for("message",check=lambda m:m.author and m.channel==ctx.channel,timeout=30.0)
        
    except asyncio.TimeoutError:
        await ctx.channel.send("You took too long!")

    else:
        if message.content.lower()=="higher":
            if number>hint:
                await ctx.send("Correct!")
            else:
                await ctx.send("Incorrect")
        elif message.content.lower()=="lower":
            if number<hint:
                await ctx.send("Correct!")
            else:
                await ctx.send("Incorrect")
        else:
            await ctx.send("Please enter higher or lower")

client.run() #this is empty as it's supposed to contain my bot's token
