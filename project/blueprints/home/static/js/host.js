const ChangeColours = () => {
    let colour = document.querySelector("body").classList[0]
    document.querySelector(":root").style.setProperty("--hostcolour", colour)

    let events = document.querySelectorAll("li")
    for (let i = 0; i < events.length; i++) {
        let colour = events[i].classList[0]
        events[i].style.setProperty("--colour", colour)
    }
}