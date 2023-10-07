import app from '../../app.js'

document.querySelectorAll('.option').forEach(option => {
    option.addEventListener('click', (e) => {
        option.id ? app.navigateTo(option.id) : false
    })
})

document.querySelector('#qr_code_button').addEventListener('click', () => {
    webapp.showScanQrPopup({text: 'Scan drawings QR code to enter on it'}, (result) => {
        webapp.showPopup({title: 'QR Code Result', message: result})
        // Verify if result contains a pattern: 'drawing_id='
        if(result.includes('drawing_id=')) {
            webapp.closeScanQrPopup()
            // Get the drawing id from the result
            const drawing_id = result.split('drawing_id=')[1]
            // Navigate to the view_drawing page passing the drawing id
            // app.navigateTo('view_enter_drawing', {id_view_drawing: drawing_id})

            // Send the drawing_id to the bot
            webapp.sendData(JSON.stringify({action: 'enter_drawing', drawing_id: drawing_id}))

        } else {
            // Show an error message
            webapp.showPopup({title: 'QR Code Result', message: 'Invalid QR Code'})
        }
    })
})

// Just for testing
console.log('GET PARAMS')
console.log(getParams())