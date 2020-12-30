import discord
import os
import requests
import json
import random
from replit import db




sad_words = ["sad", "unhappy","low", "depressed","angry", "depressing","hopeless", "gloomy","heartbroken", "miserable","downcast"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there!",
  "You are a great person!",
  "Hold on, there's always a rainbow after the rain!"
]

client = discord.Client()

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -'+json_data[0]['a']
  return quote


def update_encouragements(message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event

async def on_ready():
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content




  if msg.startswith('inspire'):
    await message.channel.send(get_quote())

  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options+db["encouragements"]
  
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New message added")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.chanel.send(encouragements)


client.run(os.getenv('TOKEN')) 
  
