document.querySelector('[name=drawing_code]').addEventListener('keyup', (e) => {
    let value = e.target.value
    if(value > 0) {
        webapp.MainButton.show()
        webapp.MainButton.text = 'ENTER DRAWING'
        webapp.MainButton.onClick(() => {
            // webapp.showPopup({title: 'Success', message: 'Drawing code entered'})
            webapp.sendData(JSON.stringify({action: 'enter_drawing', drawing_id: value}))
        })
    } else {
        webapp.MainButton.hide()
    }
})