init();

function init()
{
    addListeners();
}
function addListeners()
{
    document.getElementById("type").onchange = veriftype;
}

function veriftype()
{
    var type = document.getElementById("type");
    switch(type.options[type.selectedIndex].id)
    {
        case "QCM":
            document.getElementById("QCMdiv").style.display = "block";
            document.getElementById("RepCdiv").style.display = "none";
            document.getElementById("RepLdiv").style.display = "none";
            break;
        case "RepC":
            document.getElementById("RepCdiv").style.display = "Block";
            document.getElementById("RepLdiv").style.display = "none";
            document.getElementById("QCMdiv").style.display = "none";
            break;
        case "RepL" :
            document.getElementById("RepLdiv").style.display = "Block";
            document.getElementById("RepCdiv").style.display = "none";
            document.getElementById("QCMdiv").style.display = "none";

    }
}