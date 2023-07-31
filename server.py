from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi import Request


app = FastAPI()



def GenerateMessageList():
    chatlog = open("db/chatlog.txt", "r").read().split("\n")
    output = "<ul>"
    for line in chatlog:
        output += "<li>{}</li>".format(line)
    output += "</ul>"
    return output



@app.get("/")
async def root(r: Request):
    return FileResponse("html/root.html")

@app.get("/chatview")
async def chatview(r: Request):
    return HTMLResponse(open("html/chatview.html", "r").read().format(GenerateMessageList()))