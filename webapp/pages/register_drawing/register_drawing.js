const webapp = window.Telegram.WebApp

document.querySelector('.form').querySelectorAll('*').forEach(element => {
    element.addEventListener('keyup', e => {
        if(verifyRequiredFields()) {
            webapp.MainButton.show()
        } else {
            webapp.MainButton.hide()
        }
    })
})

webapp.MainButton.onClick(() => {
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