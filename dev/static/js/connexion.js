let modal = document.getElementById("myModal");

// Get the button that opens the modal
let boutons = document.getElementsByClassName("myBtn");
// Get the <span> element that closes the modal
let span1 = document.getElementsByClassName("close");

// When the user clicks the button, open the modal
for (let index = 0; index < boutons.length; index++) {
    const bouton = boutons[index];
    bouton.onclick = function() {
        modal.style.display = "block";
    }
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