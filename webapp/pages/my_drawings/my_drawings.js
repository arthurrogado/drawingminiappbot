const webapp = window.Telegram.WebApp;

console.log('GET PARAMS')
console.log(getParams())

let my_drawings = getParams()['my_drawings']
console.log('MY DRAWINGS')
console.log(my_drawings)


if(!my_drawings) {
    webapp.sendData(JSON.stringify({action: 'get_my_drawings'}))
}
my_drawings = JSON.parse(my_drawings.replaceAll("'", '"'))
console.log(my_drawings)

let drawingsTable = document.querySelector('#drawingsTable')
my_drawings.forEach(drawing => {
    let row = document.createElement('tr')
    row.innerHTML = `
        <td>${drawing.id}</td>
        <td>${drawing.name}</td>
    `
    row.addEventListener('click', () => {
        // alert('Nada ainda aqui :(')
        console.log('*** VIEW DRAWING ' + drawing.id)
        navigateTo('view_drawing', {id_view_drawing: drawing.id})
    })
    drawingsTable.querySelector('tbody').appendChild(row)
});