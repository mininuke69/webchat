


get_cookie();
get_ip();















function get_cookie(){
    if (document.cookie == "") {
        req = fetch("/api/cookie")
        set_cookie_to = req
        document.cookie = set_cookie_to
        console.log(set_cookie_to, req)
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