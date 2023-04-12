const ChangeColour = () => {
    let colour =  document.getElementById("colour").value
    document.getElementById("event-details-container").style.border = `5px solid ${colour}`
    document.getElementById("event-details-container").style.boxShadow = `15px 15px ${colour}`
}

const ChangeEventColour = () => {
    let box = document.getElementById("event-info")
    let colour = box.classList[1]
    box.style.setProperty('--colour', colour)
}