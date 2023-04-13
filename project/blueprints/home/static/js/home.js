const ChangeEventColours = () => {
    let events = document.getElementsByClassName("event")
    for (let n = 0; n < events.length; n++) {
        let colour = events[n].classList[1]
        events[n].style.setProperty('--colour', colour)
    }
}

