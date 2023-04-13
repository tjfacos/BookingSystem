const ChangeColour = () => {
    let colour =  document.getElementById("colour").value
    document.getElementById("event-details-container").style.border = `5px solid ${colour}`
    document.getElementById("event-details-container").style.boxShadow = `15px 15px ${colour}`
}

const ChangeEventColour = () => {
    let body = document.querySelector("body")
    let colour = body.classList[0]
    document.querySelector(":root").style.setProperty('--colour', colour)
}

const CheckPlaces = () => {
    if (!(place_left > 0)) {
        document.getElementById("book-btn").title = "Sorry! This event is already full"
        document.getElementById("book-btn").disabled = true
    }
}