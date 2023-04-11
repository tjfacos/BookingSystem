const CheckConfirmPassword = () => {
    const submit_btn = document.getElementById("password-submit")
    
    let pwd1 = document.getElementById("new-password").value
    let pwd2 = document.getElementById("confirm-password").value


    if (pwd1 == pwd2) {
        submit_btn.disabled = false
        submit_btn.title = "Change Password"
    } else {
        submit_btn.disabled = true
        submit_btn.title = "Passwords don't match!"

    }
}

const ConfigureEventsTable = () => {
    console.log("Running...")
    
    let colour_cells = document.getElementsByClassName("colour")
    console.log(colour_cells)
    for (let i = 0; i < colour_cells.length; i++) {
        let cell = colour_cells[i]
        let colour = cell.classList[1]
        console.log(cell, colour)
        console.log(colour != "None")
        if (colour != "None") {
            document.getElementById(cell.id).style.backgroundColor = colour
        }
    }

    const cells = document.querySelectorAll("td")
    for (let x = 0; x < cells.length; x++) {
        if (cells[x].innerText == "None") {
            cells[x].innerText = "-"
        }
    }
}