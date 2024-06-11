$(document).ready(function(){
    $('.message a').click(function(){
        $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    });
    const form = document.querySelector("#signinform");

    async function sendData() {
    // Associate the FormData object with the form element
    const formDataToJson = (formData) => JSON.stringify(Object.fromEntries(formData));
    const jsonData = formDataToJson(new FormData(form));
    try {
        const response = await fetch("/login", {
        method: "POST",
        // Set the FormData instance as the request body
        body: jsonData,
        headers: {'Content-Type': 'application/json'}
        });
        return await response.json();
    } catch (e) {
        console.error(e);
    }
    }

    // Take over form submission
    form.addEventListener("submit", (event) => {
    event.preventDefault();
    const resPromise = sendData();
    resPromise.then((response)=>{
        if (response){
            document.cookie = "db_session=true; max-age=60*60*24"
            window.location.href = "/";
        }
        else{
            alert("Неправильный логин или пароль")
        }
    })
    
    });
})