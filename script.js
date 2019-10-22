document.onclick = function() {
    els = document.getElementsByClassName("big-image")
    for(let i = 0; i < els.length; i++) {
        if("false" === els[i].getAttribute("active")) {
            els[i].setAttribute("active", "true")
        } else {
            els[i].remove();
        }
    }        
}
