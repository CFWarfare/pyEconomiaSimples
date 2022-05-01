from code import interact
from distutils.log import error
from ssl import VerifyFlags
import discord
import random
import asyncio
import os
import json
#-----------------


os.chdir("G:\\pyApps\\SimpleEcoBot") #Setar diretório

from dotenv import load_dotenv
from discord.ui import Button, View
from discord.ext import commands

#--------------

load_dotenv()
TOKEN = os.getenv('TOKEN') #Pegar token do .env

client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix='$',intents=discord.Intents.all())  ##Selecione prefix aqui

@bot.event #            Evento de contar servidores online
async def on_ready():
    guild_count = 0

    for guild in bot.guilds:
        guild_count =+ 1
    
    print(f"Conectado em {guild_count} guilds!")

#economia--------------------------------------------------------------

@bot.command(pass_context=True)
async def bal(ctx, user : discord.User = None): # Ver saldo
  if user != None:
    await open_account(user)
    users = await get_bank_data()
    id = user.id
    carteira_amt = users[str(id)]["carteira"]
    banco_amt = users[str(id)]["banco"]
    
    em = discord.Embed(title = f"Banco de {user.name}")
    em.add_field(name = "Saldo na Carteira: $", value = carteira_amt)
    em.add_field(name = "Saldo no Banco: $", value = banco_amt)

    await ctx.send(embed = em)
  else:
    await open_account(ctx.author)
    users = await get_bank_data()
    carteira_amt = users[str(ctx.author.id)]["carteira"]
    banco_amt = users[str(ctx.author.id)]["banco"]
  
    em = discord.Embed(title = f"Banco de {ctx.author.name}")
    em.add_field(name = "Saldo na Carteira: ", value = carteira_amt)
    em.add_field(name = "Saldo no Banco: ", value = banco_amt)

    await ctx.send(embed = em)

#@===============================

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)

async def mendigar(ctx):         # Ganhar dinheiro
  await open_account(ctx.author)
  users = await get_bank_data()
  rng1 = random.randint(1,10)
  rng2 = random.randint(0,15)

  if rng1 == 10:
   loseamt = random.randrange(1,15)
   carteirab4 = users[str(ctx.author.id)]["carteira"]

   await ctx.send(f"**Você estava mendingando na área de outro mendigo, e ele te espancou e roubou ${int(carteirab4 / loseamt)} de você!**")

   carteira_amt = users[str(ctx.author.id)]["carteira"] = users[str(ctx.author.id)]["carteira"] - int(users[str(ctx.author.id)]["carteira"] / loseamt)
    
  else:
    await ctx.send(f"**Você mendigou o dia inteiro e acabou com mais ${rng2} no bolso.**")

    carteira_amt = users[str(ctx.author.id)]["carteira"] = users[str(ctx.author.id)]["carteira"] + rng2

  
  with open("utils\\bank.json","w") as f:
    json.dump(users,f)
  return True

#@===============================

@mendigar.error                          ## Detectar erro de cooldown e avisar o usuário
async def mendigar_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        msg1 =  await ctx.reply("*Comando em cooldown!*")
        await asyncio.sleep(1)
        await msg1.delete()
        await ctx.message.delete()

#@===============================

@bot.command()
async def dep(ctx, *, valor : int):     ## Comando de depositar (para realizar um withdraw é só inverter o comando)
  await open_account(ctx.author)
  users = await get_bank_data()
  carteira_amt = users[str(ctx.author.id)]["carteira"]
  banco_amt = users[str(ctx.author.id)]["banco"]
  if valor <= carteira_amt:
    banco_amt = users[str(ctx.author.id)]["banco"] = users[str(ctx.author.id)]["banco"] + valor
    carteira_amt = users[str(ctx.author.id)]["carteira"] = users[str(ctx.author.id)]["carteira"] - valor
    await ctx.send(f"**Você depositou ${valor}**")
  else:
    await ctx.send("**Você não tem dinheiro suficiente para depositar.**")

  with open("utils\\bank.json","w") as f:
    json.dump(users,f)
  return True

#@===============================

async def open_account(user):         ## Async de criar uma conta no bank.json se o usuário não tiver uma ainda
  users = await get_bank_data()

  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["carteira"] = 0
    users[str(user.id)]["banco"] = 0

  with open("utils\\bank.json","w") as f:
    json.dump(users,f)
  return True

async def get_bank_data():          ## Async de pegar dados de todos os usuários e retornar
  with open("utils\\bank.json","r") as f:
    users = json.load(f)
  return users

#------------------------------------------------------------------------------


bot.run(TOKEN) #      Run
