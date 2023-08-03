from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi import Request
from random import randbytes
from hashlib import sha256


app = FastAPI()



def ReadDataBase():
    return open("db/chatlog.txt", "r").readlines()


def WriteDataBase(content: str):
    open("db/chatlog.txt", "a").write(content)
    database_content = open("db/chatlog.txt", "r").readlines()
    #print(len(database_content), ''.join(database_content[-5:]))
    open("db/chatlog.txt", "w").write(''.join(database_content[-10:]))


def GenerateMessageList(chatlog):
    outputHTML = "<ul>"
    for line in chatlog:
        outputHTML += "<li>{}</li>".format(line)
    outputHTML += "</ul>"
    return outputHTML


# HTML

@app.get("/")
async def root(r: Request):
    return FileResponse("html/chat.html")


# JavaScript

@app.get("/js/main.js")
async def mainjs(r: Request):
    return FileResponse("js/main.js")


# CSS

@app.get("/css/style.css")
async def stylecss(r: Request):
    return FileResponse("css/style.css")


# API

@app.post("/api/sendmsg")
async def sendmsg(r: Request):
    id = r.cookies["id"]
    message_bytes: bytes = await r.body()
    message_obj = eval(message_bytes.decode())
    message_content: str = message_obj["content"]

    print(f'message received: "{message_content}", cookie: "{id[:6]}...{id[-6:]}"')

    if not message_content == "":
        WriteDataBase(message_content + "\n")

    return None


@app.get("/api/cookie")
async def cookie(r: Request):
    generate_id = sha256(randbytes(16)).hexdigest()
    return f'id={generate_id}'


@app.get("/api/ip")
async def ip(r: Request):
    headers = r.headers
    ip_addr = headers["host"]
    return ip_addr


@app.get("/api/chatlog")
async def chatlog(r: Request, contenttype: str | None = None):
    if contenttype.lower() == "html":
        return GenerateMessageList(ReadDataBase())
    else:
        return ReadDataBase()