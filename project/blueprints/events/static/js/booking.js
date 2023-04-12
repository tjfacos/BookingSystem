var guest_index = 1

const AddGuest = () => {
    const GuestTable = document.getElementById("guest-list")
    let row = GuestTable.insertRow()
    row.classList.add("guest-row")
    row.id = `guest_${++guest_index}`
    let name_cell = row.insertCell()
    let age_cell = row.insertCell()
    let delete_cell = row.insertCell()

    name_cell.innerHTML = `<input type=\"text\" name=\"guest_${guest_index}_name\" required>`
    age_cell.innerHTML = `<input type=\"number\" id=\"guest_${guest_index}_age\" name=\"guest_${guest_index}_age\" required onchange="CheckAges(${guest_index})">`
    delete_cell.innerHTML = `<button onclick="RemoveGuest(${guest_index})" class="guest-remove-btn" type="button">Remove Guest</button>`

    document.getElementById("book-btn").setCustomValidity("")
}

const RemoveGuest = (index) => {
    const GuestTable = document.getElementById("guest-list")
    for (let i = 0; i < GuestTable.rows.length; i++) {
        if (GuestTable.rows[i].id == `guest_${index}`) {
            GuestTable.rows[i].remove()
        }
    }

    if (GuestTable.rows.length == 1) {
        document.getElementById("book-btn").setCustomValidity("There must be at least 1 guest")
    }
}

const CheckAges = (index) => {
    let age = document.getElementById(`guest_${index}_age`).value
    if (age < agelimit) {
        document.getElementById(`guest_${index}_age`).setCustomValidity("The guest is too young")
    } else {
        document.getElementById(`guest_${index}_age`).setCustomValidity("")
    }
}