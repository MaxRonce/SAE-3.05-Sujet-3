init();

function init()
{
    addListeners();
}
function addListeners()
{
    document.getElementById("is_template").onchange = veriftype;
}



function toggleBoxVisibility() {

if (document.getElementById("check").checked == true) {

    document.getElementById("pointneg").style.display = "flex";

    }
else {

    document.getElementById("pointneg").style.display = "none";

    }
}


function toggletemplateBoxVisibility() {

if (document.getElementById("checkt").checked == true) {

    document.getElementById("templatef").style.display = "flex";

    }
else {

    document.getElementById("templatef").style.display = "none";

    }
}

