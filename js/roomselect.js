

async function submitroom(event) {
    if (event.keyCode == 13) {
        const roominput = document.getElementById("roomid")
        let roomid = roominput.value

        location.href = "/room_" + roomid
    }
}