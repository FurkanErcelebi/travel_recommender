
var planDetailModal = new bootstrap.Modal(document.getElementById('planDetailModal'));
var popupWarningModal = new bootstrap.Modal(document.getElementById('popup-warning'));

var plan_list = [];
let indexOfPlan;
    
var start_offset = 0;
var container = document.getElementsByClassName("container")[1];
container = container.childNodes[1];
container.textContent = '';

function loadRecommendedTripPlans() {
    
    request_settings.url = "http://localhost:8000/rcm_plans/get-host-trip-plan";
    request_settings.method = "GET";

    $.ajax(request_settings).done(function (response) {
        plan_list = plan_list.concat(response.hosts_and_trip_places);
        add_plans_to_the_page();
    });
}

loadRecommendedTripPlans();

/*<div class="spinner-border m-5" role="status">
  <span class="visually-hidden">Loading...</span>
</div>*/
var spinner = document.createElement("span")
spinner.className = "visually-hidden";
spinner.innerHTML = "Loading...";
var spinnerDiv = document.createElement("div")
spinnerDiv.className = "spinner-border"; //m-5
spinnerDiv.style.cssText = "margin-left: 50% !important;";
spinnerDiv.role = "status";
spinnerDiv.appendChild(spinner);

function set_spinner(){
	container.appendChild(spinnerDiv);
	console.log("you're at the bottom of the page");
	new Promise(r => setTimeout(r, 8000));
}

set_spinner();

var refreshBtn = document.getElementById("refresh");
makeHOstNameShorter();

refreshBtn.addEventListener("click", function() {
    container.textContent = '';
    plan_list = [];
    start_offset = 0;
    set_spinner();
    loadRecommendedTripPlans();
});

window.onscroll = function(ev) {
    if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
        loadRecommendedTripPlans();
        set_spinner();
    }
};

function makeHOstNameShorter(){
    
    let hostInfos = document.getElementsByClassName("hostInfo");

    if(hostInfos.length > 0){
        for (const hostInfo of hostInfos) {
            let host_name = hostInfo.innerHTML;
            if(host_name.length > 20){
                host_name = host_name.substring(0, 20) + "...";
                hostInfo.innerHTML = host_name;
            }
            console.log(hostInfo.innerHTML)
            console.log(hostInfo.value)
        }
    }

}



function add_plans_to_the_page(){
    
    if(container.getElementsByClassName("spinner-border").length > 0){
        container.removeChild(spinnerDiv);
    }

    for (let index = start_offset; index < start_offset + 18; index++) {
        
        let the_plan = plan_list[index];

        let place_url_list = the_plan.trip_places.flatMap((x) => x.photo_url_list);

        let img_divs = [];
        if(place_url_list.length > 0){
            let isfirst = true;
            place_url_list.forEach((photo_url) => {
                img_divs.push(`<div class="carousel-item${isfirst ? ' active' : ''}" data-bs-interval="5000">
                                <img height="225" class="d-block w-100" src="${photo_url}" />
                               </div>`);
                if(isfirst)
                    isfirst = !isfirst;
            });
        }
        else {
            img_divs.push(`<div class="carousel-item active" data-bs-interval="5000">
                                <svg class="bd-placeholder-img card-img-top" width="100%" height="225" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder: Thumbnail" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="#55595c"/><text x="50%" y="50%" fill="#eceeef" dy=".3em">No Image Found</text></svg>
                            </div>`);
        }

        host_name = the_plan.host_infos.name;
        host_name = host_name.length > 20 ? `${host_name.substring(0, 20)}...` : host_name
        const trip_plan= elementFromHTML(`<div class="col">
                                            <div class="card shadow-sm">
                                                <div id="tripPlan_${index.toString()}" class="carousel slide tripPlanDiv" data-bs-ride="carousel">
                                                    <div class="carousel-inner">
                                                        ${img_divs.join('\n')}
                                                    </div>
                                                </div>

                                                <div class="card-body">
                                                    <p class="card-text">This is trip plan for ${host_name}</p>
                                                    <div class="d-flex justify-content-between align-items-center">
                                                        <div class="btn-group">
                                                            <button type="button" class="btn btn-sm btn-outline-secondary view_button" >View</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>`);
        //<button type="button" class="btn btn-sm btn-outline-secondary view_button" data-bs-toggle="modal" data-bs-target="#planDetailModal" >View</button>
        container.appendChild(trip_plan);
    }
	
	var tripPlanDivs = [...document.querySelectorAll('.tripPlanDiv')];
    tripPlanDivs.forEach((tripPlanDiv) =>{
        new bootstrap.Carousel(tripPlanDiv, {
            wrap: true
        });
    });

    start_offset += 18;
}

$(document).on("click", ".view_button", (event) => {
    let indexOfPlan = parseInt(event.target.parentNode.parentNode.parentNode.parentNode.children[0].id.split('_')[1]);
    operateOnPlan(indexOfPlan);
});

