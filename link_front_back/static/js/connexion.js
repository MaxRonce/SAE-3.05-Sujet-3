let modal = document.getElementById("myModal");
let modal2 = document.getElementById("registerModal");

// Get the button that opens the modal
let boutons = document.getElementsByClassName("myBtn");
// Get the <span> element that closes the modal
let span1 = document.getElementsByClassName("close");

function openModal() {
    modal2.style.display = "none";
    modal.style.display = "block";
}

function openModal2() {
    modal.style.display = "none";
    modal2.style.display = "block";
}



// When the user clicks the button, open the modal
for (let index = 0; index < boutons.length; index++) {
    const bouton = boutons[index];
    bouton.onclick = openModal;
}

// When the user clicks on <span> (x), close the modal
for (let index = 0; index < span1.length; index++) {
    const span = span1[index];
    span.onclick = function() {
        modal.style.display = "none";
    }
}

window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}
