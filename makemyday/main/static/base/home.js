
const studentLoginBtn = document.getElementById("student-login-button")
const instructorLoginBtn = document.getElementById("instructor-login-button")
const signUpBtn = document.getElementById("register-button")
const url = window.location.href

function goToLogin(){
    window.location.href = url + "login"
}

studentLoginBtn.addEventListener('click', goToLogin)

instructorLoginBtn.addEventListener('click', goToLogin)

signUpBtn.addEventListener('click', ()=>{
    window.location.href = url + "register/"
})