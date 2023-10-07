let drawingsInfo = getParams()['drawings_on_info']
drawingsInfo = JSON.parse(drawingsInfo.replaceAll("'", '"'))
console.log('DRAWINGS ON INFO')
console.log(drawingsInfo)

console.log('GET PARAMS')
console.log(getParams())

drawingsInfo.find(drawingInfo => {
    if(drawingInfo.id == getParams()['id_view_drawing']) {
        document.querySelector('#drawingId').innerHTML = drawingInfo.id
        document.querySelector('[name=name]').value = drawingInfo.name
        document.querySelector('[name=description]').value = drawingInfo.description
        document.querySelector('#numberOfParticipants').innerHTML = drawingInfo.participants
        document.querySelector('.qrcode img').src = generateQrCode(`drawing_id=${drawingInfo.id}`)
    }
})

// LEAVE

document.querySelector('#leaveDraw').addEventListener('click', () => {
    webapp.showConfirm("Are you sure you want to leave this drawing?", (press) => {
        if(!press) return 
        webapp.sendData(JSON.stringify({
            action: 'leave_drawing',
            drawing_id: getParams()['id_view_drawing']
        }))
    })
})

// Use Google Charts to generate a QR Code
function generateQrCode(text) {
    let apiGoogleCharts = 'https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl='
    return apiGoogleCharts + text
}

// SHARING

let url = "https://t.me/drawingsminiappbot?start=drawing_id=" + getParams()['id_view_drawing']
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