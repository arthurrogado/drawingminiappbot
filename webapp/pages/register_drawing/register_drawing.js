const webapp = window.Telegram.WebApp


function register() {
    if(!verifyRequiredFields()) {
        return
    }

    const data = new FormData(document.querySelector('.form'))
    const json = {
        'action': 'register_drawing',
        'name': data.get('name'),
        'description': data.get('description'),
    }
    webapp.sendData(JSON.stringify(json))
}


document.querySelector('.form').querySelectorAll('*').forEach(element => {
    element.addEventListener('input', e => {

        webapp.MainButton.text = "REGISTER"
        window.defineMainButtonCallback(register) // function to set the main button callback (see app.js)

        if(verifyRequiredFields()) {
            webapp.MainButton.show()
        } else {
            webapp.MainButton.hide()
        }
    })
})






// document.querySelector('.form').addEventListener('submit', (e) => {
//     e.preventDefault()

//     const data = new FormData(e.target)
//     const json = {
//         'action': 'register_drawing',
//         'name': data.get('name'),
//         'description': data.get('description'),
//     }
//     webapp.sendData(JSON.stringify(json))
// })