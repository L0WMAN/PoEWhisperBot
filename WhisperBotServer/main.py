import os
import discord
import discord.ext.tasks as tasks
from dotenv import load_dotenv
import asyncio
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
UID = os.getenv('USER_ID')
bot = discord.Client()

class Message(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start(TOKEN))
    await asyncio.sleep(5)
    print(f'{bot.user} has connected to Discord!')
    
@app.post("/")
async def getMsg(msg : Message):
    await send_message(msg.message)
    return {"message": f"'{msg}' sent"}
    

async def send_message(msg):
    user = await bot.fetch_user(UID)
    await user.send(msg)  

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
