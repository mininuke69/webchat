

get_cookie();
const roomid = sessionStorage.getItem("roomid")
setInterval(updatechatlog, 5000)
updatechatlog()


async function get_cookie(){
    if (document.cookie == "") {
        req = await fetch("/api/cookie")
        document.cookie = await req.json()
    }
}


async function submitmessage(event) {
    if (event.keyCode == 13) {
        console.log("submitting message");
        
        const messagebar = document.getElementById("messagebar")
        let message = messagebar.value;
        messagebar.value = ""

        let messageitem = {
            content: message,
            roomid: roomid,
            date: new Date(Date.now()),
        }

        let reply = await fetch("/api/sendmsg", {
            method: "POST",
            headers: {"content-type": "application/json"},
            body: JSON.stringify(messageitem)
        });

        console.log("reply: " + await reply.json());
    }
}

async function updatechatlog() {
    const chat = document.getElementById("chatlog")

    let reply = await fetch("/api/chatlog?contenttype=html&roomid=" + roomid)
    chat.innerHTML = await reply.json()
}