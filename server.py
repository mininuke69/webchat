from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi import Request
from random import randbytes
from hashlib import sha256


app = FastAPI()



def GenerateMessageList():
    chatlog = open("db/chatlog.txt", "r").read().split("\n")
    output = "<ul>"
    for line in chatlog:
        output += "<li>{}</li>".format(line)
    output += "</ul>"
    return output


# HTML

@app.get("/")
async def root(r: Request):
    return FileResponse("html/root.html")


# JavaScript

@app.get("/js/main.js")
async def mainjs(r: Request):
    return FileResponse("js/main.js")


# CSS

@app.get("/css/style.css")
async def stylecss(r: Request):
    return FileResponse(path)


# API

@app.post("/api/sendmsg")
async def sendmsg(r: Request):
    cookie = r.cookies["id"]
    message_bytes = await r.body()
    message_obj = eval(message_bytes.decode())
    message_content, message_date = message_obj["content"], message_obj["date"]
    print(f'message received: "{message_content}", cookie: "{cookie[:6]}...{cookie[-6:]}"')
    open("db/chatlog.txt", "a").write(message_content + "\n")
    return f'message received: {message_content}'


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
        return GenerateMessageList()
    else:
        return open("db/chatlog.txt", "r").readlines()