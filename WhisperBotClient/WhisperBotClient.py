import asyncio
from fastapi import FastAPI
from queue import Queue
import requests
from pydantic import BaseModel

lineno = 121190
lastLine = lineno
msgQueue = Queue(maxsize = 0)
path = 'C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs\Client.txt'

class Message(BaseModel):
    message: str

async def watch(file, lineno): #line number of last read line
    line = ''
    for i in range(lineno): #skip first number of lines that have already been read
        next(file)
    
    while True:
        tmp = file.readline()
        if tmp is not None:
            line += tmp
            if line.endswith("\n"):
                yield line
                line = ''
        else:
            asyncio.sleep(0.1)

async def parse(msgQueue):
    async for line in watch((open(path, 'r', encoding='utf-8')), lastLine):
        splitIdx = line.find("@From")
        ++lastLine
        if splitIdx > -1:
            if line != '':
                incMsg = line[splitIdx+6:].strip() #extra newline why?
                msgQueue.put(incMsg)
                print(line[splitIdx+6:], end='')
                #postMsg()
                while not (msgQueue.empty()):
                    tempMsg = msgQueue.get()
                    print("Sending : " + tempMsg)
                    r = requests.post('http://127.0.0.1:8000/', json = {"message" : tempMsg})                  


async def main():
    await asyncio.sleep(1)
    asyncio.create_task(parse(msgQueue))
   

asyncio.run(main())