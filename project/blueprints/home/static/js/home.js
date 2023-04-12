const ChangeEventColours = () => {
    let events = document.getElementsByClassName("event")
    for (let n = 0; n < events.length; n++) {
        let colour = events[n].classList[1]
        events[n].style.setProperty('--colour', colour)
    }

    
    // let colour =  document.getElementById("colour").value
    // document.getElementById("event-details-container").style.border = `5px solid ${colour}`
    // document.getElementById("event-details-container").style.boxShadow = `15px 15px ${colour}`
}