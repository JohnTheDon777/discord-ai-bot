import discord
import os
from openai import OpenAI

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are Luna, a soft playful gamer e-girl.
You respond casually, a bit teasing, friendly, never explicit.
Keep responses short and engaging.
"""

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        user_message = message.content.replace(f"<@{client.user.id}>", "").strip()

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        await message.channel.send(response.choices[0].message.content)

client.run(os.getenv("DISCORD_TOKEN"))
