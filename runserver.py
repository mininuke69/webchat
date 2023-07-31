from uvicorn import run as runserver
from subprocess import PIPE
from subprocess import run as runcmd

print("getting ip...")
process = runcmd(["hostname", "-I"], stdout=PIPE, text=True)
ipv4 = process.stdout.split(" ")[0]
port = 8808

print(f'starting server on ip {ipv4}, port {port}')
runserver("server:app", host=ipv4, port=port)