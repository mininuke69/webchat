

get_cookie();
setInterval(updatechatlog, 2000)



async function get_cookie(){
    if (document.cookie == "") {
        req = await fetch("/api/cookie")
        document.cookie = await req.json()
    }
}

function get_ip(){
    let ip = fetch("/api/ip")
    console.log(ip)
}



async function submitmessage() {
    console.log("submitting message");
    
    const messagebar = document.getElementById("messagebar")
    let message = messagebar.value;

    let messageitem = {
        content: message,
        date: new Date(Date.now()),
    }

    let reply = await fetch("/api/sendmsg", {
        method: "POST",
        headers: {"content-type": "application/json"},
        body: JSON.stringify(messageitem)
    });

    console.log("reply: " + await reply.json());
}

async function updatechatlog() {
    console.log("updating chat...")

    const chat = document.getElementById("chatlog")

    let reply = await fetch("/api/chatlog?contenttype=html")
    chat.innerHTML = await reply.json()
    
}