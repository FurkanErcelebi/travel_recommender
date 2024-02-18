
if(location.pathname.endsWith("account")){
    document.getElementsByClassName("editButtonDiv")[0].hidden = true;
}


if(location.pathname.endsWith("calender")){
    document.getElementById("editButton").innerHTML = "Add plan";
}


// let alerts = document.querySelector(".alertBox");

// for (const alert of   [].slice.call(alerts)) {
//     alert.hidden = true;
// }