from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi import Request
from random import randbytes
from hashlib import sha256
from string import ascii_letters


app = FastAPI()

DB_PATH = "db/chatlog_{}.txt"

def ReadDataBase(roomid: int):
    try:
        return open(DB_PATH.format(roomid), "r").readlines()
    except FileNotFoundError:
        open(DB_PATH.format(roomid), "w")
        for _ in range(10): open(DB_PATH.format(roomid), "a").write("\n")
        return open(DB_PATH.format(roomid), "r").readlines()


def WriteDataBase(roomid: int, content: str):
    open(DB_PATH.format(roomid), "a").write(content + "\n")
    database_content = open(DB_PATH.format(roomid), "r").readlines()
    open(DB_PATH.format(roomid), "w").write(''.join(database_content[-10:]))


def GenerateMessageList(chatlog):
    outputHTML = "<ul>"
    for line in chatlog:
        outputHTML += "<li>{}</li>".format(line)
    outputHTML += "</ul>"
    return outputHTML


# HTML

@app.get("/")
async def root(r: Request):
    return FileResponse("html/roomselect.html")


@app.get("/chat")
async def room(r: Request):
    return FileResponse("html/chat.html")


# JavaScript

@app.get("/js/chat.js")
async def chatjs(r: Request):
    return FileResponse("js/chat.js")

@app.get("/js/roomselect.js")
async def roomselectjs(r: Request):
    return FileResponse("js/roomselect.js")


# CSS

@app.get("/css/style.css")
async def stylecss(r: Request):
    return FileResponse("css/style.css")


# API

@app.post("/api/sendmsg")
async def sendmsg(r: Request):

    """
    called when a message is sent using a post request to /api/sendmsg

    reads the POST body, which should contain content and roomid
    does a couple of checks on max message size and if it contains a visible character
    writes the message to the desired room using WriteDataBase()

    """

    id = r.cookies["id"]
    message_bytes: bytes = await r.body()
    message_obj = eval(message_bytes.decode())
    message_content: str = message_obj["content"]
    roomid: str = message_obj["roomid"]

    print(f'message received: "{message_content}", cookie: "{id[:6]}...{id[-6:]}"')

    for index, letter in enumerate(message_content): #check is at least one character is not a space
        if letter in ascii_letters:
            break
        if index == len(message_content) - 1:
            return
    
    if len(message_content) > 80:
            return
    
    WriteDataBase(roomid, message_content)

    return None


@app.get("/api/cookie")
async def cookie(r: Request):
    """
    generates a new cookie by hashing 16 random bytes
    currently has no real use
    """

    generate_id = sha256(randbytes(16)).hexdigest()
    return f'id={generate_id}'


@app.get("/api/ip")
async def ip(r: Request):
    """
    returns the ip of the user. currently has no use
    """

    headers = r.headers
    ip_addr = headers["host"]
    return ip_addr


@app.get("/api/chatlog")
async def chatlog(r: Request, contenttype: str = None, roomid: str = None):
    """
    returns the chatlog in a <ul> tag or in plaintext format
    """

    if contenttype.lower() == "html":
        return GenerateMessageList(ReadDataBase(roomid))
    else:
        return                     ReadDataBase(roomid)