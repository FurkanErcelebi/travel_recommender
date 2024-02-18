
var host_list = [];
var keyword = '';

var getListRequestBody = {
    start_offset: 0,
    length: 20
}


request_settings.url = "http://localhost:8000/host_info/get-list";
request_settings.method = "POST";
request_settings.data = JSON.stringify(getListRequestBody);

add_hosts_to_the_page();


var spinner = document.createElement("span")
spinner.className = "visually-hidden";
spinner.innerHTML = "Loading...";
var spinnerDiv = document.createElement("div")
spinnerDiv.className = "spinner-border m-5";
spinnerDiv.role = "status";
spinnerDiv.appendChild(spinner);


window.onscroll = function(ev) {
    if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
        add_hosts_to_the_page();
    
        var listTag = document.getElementsByTagName('ul')[1];
        listTag = listTag.parentElement;
        listTag.appendChild(spinnerDiv);
        console.log("you're at the bottom of the page");
        new Promise(r => setTimeout(r, 4000));
    }
};

function makeHostNameShorter(){
    
    let hostName = document.getElementsByClassName("hostName")[0];

    if(hostName.length > 0){
        for (const hostInfo of hostName) {
            let host_name = hostInfo.innerHTML;
            if(host_name.length > 40){
                host_name = host_name.substring(0, 40) + "...";
                hostInfo.innerHTML = host_name;
            }
            console.log(hostInfo.innerHTML)
            console.log(hostInfo.value)
        }
    }

}

function elementFromHTML(html){
    const template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.firstElementChild;
}


function add_hosts_to_the_page(){

    var listTag = document.getElementsByTagName('ul')[1];
    var listDiv = listTag.parentElement;
    
    if(listDiv.getElementsByClassName("spinner-border").length > 0){
        listDiv.removeChild(spinnerDiv);
    }



    $.ajax(request_settings).done(function (response) {
        for (let host_info of response.host_info_list) {
        
            const host_brief_info= elementFromHTML(`<li class="list-group-item">
                                                        <a href=${host_info.url_page} class="list-group-item list-group-item-action">
                                                        <div class="hostBriefs">
                                                            <div class="hostName">
                                                                <p>
                                                                    ${host_info.name.length > 100 ? host_info.name.substring(0,37) + '...': host_info.name}
                                                                </p>
                                                            </div>
                                                            <div class="hostRate1">
                                                                <h6>rate:  ${host_info.rate}</h6>
                                                            </div>
                                                        </div>
                                                        </a>
                                                    </li>`);
            
            listTag.appendChild(host_brief_info);
        }
    });
    getListRequestBody.start_offset += getListRequestBody.length;
    request_settings.data = JSON.stringify(getListRequestBody);

}

document.getElementById('hostSearchButton').addEventListener('click', () => {
    keyword = document.getElementById('hostSearchInput').value;
    getListRequestBody.keyword = keyword;
    getListRequestBody.start_offset = 0;
    request_settings.data = JSON.stringify(getListRequestBody);
    host_list = [];
    document.getElementsByTagName('ul')[1].innerHTML = "";
    add_hosts_to_the_page();
})


