const profile_id = JSON.parse(document.getElementById("profile_id").textContent)

window.onload = function() {
    if (document.querySelector('.image-container')) {
        make_call()
    }
}

function make_call() {
    const req = new XMLHttpRequest()
    req.onreadystatechange = function() {
        if (this.readyState === 4) {
            let data = JSON.parse(this.responseText)
            data.forEach((image, idx) => {
                console.log(image)
                let my_html = '<div>'
                my_html += `<img class="image__item image__item--${idx+1}" src=${image.image} alt=${image.name}>`
                my_html += '</div>'
                document.querySelector('.image-container').innerHTML += my_html
            })
        }
    }
    req.open('GET', `/api/images/${profile_id}`,true)
    req.send()
}
