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