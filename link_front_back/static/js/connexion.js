let modal = document.getElementById("myModal");

// Get the button that opens the modal
let btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
let span1 = document.getElementsByClassName("close")[0];

let login = document.getElementById("button_slider");

// When the user clicks the button, open the modal
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span1.onclick = function() {
    modal.style.display = "none";
}

login.onclick = function () {
    window.location.href = "https://stackoverflow.com";

}
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}