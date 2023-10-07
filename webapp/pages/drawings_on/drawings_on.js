const webapp = window.Telegram.WebApp;

let params = getParams()

// Verify if the params are valid, if not respond to bot to get drawings_on (and drawings_on_info)
let drawings_on = params['drawings_on']
if(!drawings_on) { webapp.sendData(JSON.stringify({action: 'get_drawings_on'}))}

drawings_on = JSON.parse(drawings_on.replaceAll("'", '"'))
console.log('DRAWINGS ON')
console.log(drawings_on)

let drawings_on_info = JSON.parse(params['drawings_on_info'].replaceAll("'", '"'))
console.log('DRAWINGS ON INFO')
console.log(drawings_on_info)

let drawingsTable = document.querySelector('#drawingsTable')
drawings_on.forEach(drawing => {
    let row = document.createElement('tr')
    // find the drawing info in drawings_on_info with the same id as the drawing that we are iterating and user is participating
    let drawing_info = drawings_on_info.find(drawing_info => drawing_info.id == drawing.id_drawing)
    row.innerHTML = `
        <td>
            ${drawing_info.name}
        </td>
    `
    row.addEventListener('click', () => {
        navigateTo('view_drawing_on', {id_view_drawing: drawing_info.id})
    })
    drawingsTable.querySelector('tbody').appendChild(row)
});