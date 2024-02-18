

var url = $(location).attr('href');
if(!url.endsWith('get-list')){
    $('.searchHost').remove();
}

let rangeInput = document.getElementById("rateButton");
var rateValue = document.getElementById("rateValue");
rateValue.innerText = rangeInput.value;

rangeInput.addEventListener("change", function() {

    rateValue.innerText = rangeInput.value;
    let host_id = url.substring(url.lastIndexOf('/') + 1);
    
    request_settings.url = "http://localhost:8000/host_info/set-rate";
    request_settings.method = "POST";
    request_settings.data = JSON.stringify({
      "host_id": host_id,
      "rate_score": rangeInput.value
    });
      
    $.ajax(request_settings).done(function (response) {
        console.log(response);
    });
}, false);


