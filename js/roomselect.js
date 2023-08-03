

async function submitroom(event) {
    if (event.keyCode == 13) {
        const roominput = document.getElementById("roomid")
        let roomid = roominput.value
        
        sessionStorage.setItem("roomid", roomid)
        location.href = "/chat"
    }
}