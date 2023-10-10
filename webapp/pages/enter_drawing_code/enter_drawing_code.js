
function enterCode() {
    let value = document.querySelector('[name=drawing_code]').value

    webapp.showPopup({title: 'Success', message: 'Drawing code entered: ' + value})
    webapp.sendData(JSON.stringify({action: 'enter_drawing', drawing_id: value}))
}


document.querySelector('[name=drawing_code]').addEventListener('input', (e) => {
    let value = e.target.value

    window.defineMainButtonCallback(enterCode)
    
    if(value > 0) {
        
        webapp.MainButton.text = 'ENTER DRAWING'
        webapp.MainButton.show()

    } else {
        webapp.MainButton.hide()
    }
})