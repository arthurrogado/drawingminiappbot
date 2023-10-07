// view_drawings.js

// This is a page to the owner of the drawing see it
// the owner can see and update details, delete the drawing,
// as well as its participants
//==========================================================

// just to know where this functions are called from
// but it is already global
import app from "../../app.js"
// let getParams = app.getParams

// get params just make an object with all url params:
// like: 'id=1&name=2' turns into {id: 1, name: 2}
console.log('GET PARAMS')
console.log(getParams())

let my_drawings = getParams()['my_drawings']
console.log('MY DRAWINGS')
console.log(my_drawings)

// now we can parse it to a json object
my_drawings = my_drawings.replaceAll("'", '"')
console.log('MY DRAWINGS REPLACE SINGLE QUOTES')
console.log(my_drawings)

let drawingsObj = JSON.parse(my_drawings)
console.log('DRAWINGS OBJ')
console.log(drawingsObj)

// now we can use it
// finding the drawing with the id passed in the url in the drawingsObj
// then populating the fields with the drawing data
drawingsObj.find(drawing => {
    if(drawing.id == getParams()['id_view_drawing']) {
        document.querySelector('#drawingId').innerHTML = drawing.id
        document.querySelector('[name=name]').value = drawing.name
        document.querySelector('[name=description]').value = drawing.description
        document.querySelector('#numberOfParticipants').innerHTML = drawing.participants
        document.querySelector('.qrcode img').src = generateQrCode(`drawing_id=${drawing.id}`)
    }
})

let editButton = document.querySelector('#edit')

const startEdit = () => {
    // enable the fields
    document.querySelectorAll('.form > *').forEach(element => {
        element.removeAttribute('disabled')
    })

    document.querySelectorAll('.card').forEach(card => {
        if(card.classList.contains('view_drawing')){ return }
        card.style.display = 'none'
    })
    
    editButton.style.background = 'orange'
    editButton.innerHTML = 'Cancel editing'
    editButton.removeEventListener('click', () => {this})
    editButton.addEventListener('click', endEdit)
    
    webapp.MainButton.show()
    webapp.MainButton.setText('SAVE')
    webapp.MainButton.color = '#13e95a'
    webapp.MainButton.onClick(() => {
        if(!verifyRequiredFields()) {
            webapp.showPopup({title: 'Error', message: 'Fill all required fields'})
            return
        }
        const data = new FormData(document.querySelector('.form'))
        const json = {
            'action': 'update_drawing',
            'id': getParams()['id_view_drawing'],
            'name': data.get('name'),
            'description': data.get('description'),
        }
        webapp.sendData(JSON.stringify(json))
    })
}

const endEdit = () => {
    //- Cancel editing process
    // hide the main button
    webapp.MainButton.hide()

    document.querySelectorAll('.card').forEach(card => {
        card.style.display = ''
    })

    // disable the fields
    document.querySelectorAll('.form > *').forEach(element => {
        element.setAttribute('disabled', 'true')
        webapp.MainButton.hide()
    })
    // change the button color to the default
    editButton.style.background = webapp.themeParams.button_color
    editButton.innerHTML = 'Edit'
    // change the button event listener to startEdit
    editButton.removeEventListener('click', endEdit)
    editButton.addEventListener('click', startEdit)
}

editButton.addEventListener('click', startEdit)


// DELETE

let deleteButton = document.querySelector('#delete')

const startDelete = () => {
    webapp.showPopup({
        title: 'Delete drawing',
        message: 'Are you sure you want to delete this drawing?',
        buttons: [
            {
                text: 'Yes',
                type: 'destructive',
                id: 'sendDeleteAction'
            },
            {
                text: 'No',
            }
        ]
    }, action => {
        if(action == 'sendDeleteAction') {
            webapp.sendData(JSON.stringify({
                action: 'delete_my_drawing',
                drawing_id: getParams()['id_view_drawing']
            }))
        }
    })
}

deleteButton.addEventListener('click', startDelete)



// Use Google Charts to generate a QR Code
function generateQrCode(text) {
    let apiGoogleCharts = 'https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl='
    return apiGoogleCharts + text
}

// SHARING

let botUsername = getParams()["bot_username"]
console.log('BOT USERNAME')
console.log(botUsername)

let url = "https://t.me/" + getParams()["bot_username"] + "?start=drawing_id=" + getParams()['id_view_drawing']
let text = "Join this drawing on Drawings Mini App!"
let shareLink = `https://t.me/share/url?url=${url}&text=${text}`
document.querySelector('#shareLink').addEventListener('click', () => {
    webapp.openTelegramLink(shareLink)
})

// Function to copy content from #drawingId to clipboard
function copyToClipboard() {
    let text = document.querySelector('#drawingId').innerHTML
    navigator.clipboard.writeText(text)
    webapp.showPopup({title: 'Success', message: 'Drawing id copied to clipboard'})
}
document.querySelector('#drawingIdCard').addEventListener('click', copyToClipboard)

// DRAW
document.querySelector('#doDrawing').addEventListener('click', () => {
    // send to backend that the user wants to draw
    webapp.sendData(JSON.stringify({
        action: 'do_drawing',
        drawing_id: getParams()['id_view_drawing']
    }))
})