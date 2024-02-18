
function operateOnPlan(indexOfPlan) {
    planDetailModal.show();
    let inRecommenderPage = window.location.href.includes('rcm_plans')
    let operateTripPlanButton = document.getElementById('operateTripPlan');
    operateTripPlanButton.innerText = inRecommenderPage ? 'Add Plan To Calender' : 'Remove Plan From Calender';

    operateTripPlanButton.className = inRecommenderPage ? 'btn btn-primary' : 'btn btn-danger';

    let the_plan = plan_list[indexOfPlan];
    let planId = the_plan.id;

    let hostBriefInfoList =  document.getElementById('host_infos');
    [hostBriefInfoList].forEach((hostBriefInfo) => {
        let paragraphs = hostBriefInfo.getElementsByTagName('p');
        paragraphs[0].innerText =  the_plan.host_infos.name
        paragraphs[1].innerText =  the_plan.host_infos.review_scores_rating
        paragraphs[2].innerText =  the_plan.host_infos.price
        paragraphs[3].innerText =  the_plan.host_infos.property
    });

    document.getElementsByClassName('viewHost')[0].children[0].setAttribute('href', the_plan.host_url);

    if(!inRecommenderPage){
        document.getElementById('startDatePicker').disabled = true
        document.getElementById('endDatePicker').disabled = true
    }

    let currentDate = new Date();
    todayDate = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()}`;

    // remove when submit
    
    $(function() {
        $('#startDatePicker').datepicker('setStartDate', todayDate)
        let date_tokens = the_plan.start_date.split('-')
        $('#startDatePicker').datepicker('update', `${date_tokens[2]}-${date_tokens[1]}-${date_tokens[0]}`)
        $('#startDatePicker').on('changeDate', function(ev){
            console.log(ev.date.valueOf());
            });
    });
    
    $(function() {
        $('#endDatePicker').datepicker('setStartDate', todayDate)
        let date_tokens = the_plan.end_date.split('-')
        $('#endDatePicker').datepicker('update', `${date_tokens[2]}-${date_tokens[1]}-${date_tokens[0]}`)
        .on('changeDate', function(ev){
            console.log(ev.date.valueOf());
            });
    });
    // remove when submit
        

    let rangeInput = document.getElementById('rateButton');
    let rateValue = document.getElementById("rateValue");
    rateValue.innerText = rangeInput.value;
    if (new Date() > new Date(the_plan.end_date)) {

      rateValue.innerText = rangeInput.value;
      document.getElementsByClassName('planRate')[0].hidden = false;
      if (the_plan.trip_rate) {
          rangeInput.value = the_plan.trip_rate;
      }
      rangeInput.addEventListener("change", function() {
        rateValue.innerText = rangeInput.value;
        request_settings.url = "http://localhost:8000/trip_plans/set-rate";
        request_settings.method = "POST";
        request_settings.data = JSON.stringify({
            "plan_id": planId,
            "rate_score": rangeInput.value
        });
        
        $.ajax(request_settings).done(function (response) {
            console.log(response);
        });
      }, false);
      document.getElementById('operateTripPlan').hidden = true;
    }
    else {
      document.getElementsByClassName('planRate')[0].hidden = true;
      document.getElementById('operateTripPlan').hidden = false;
    }

    let place_types_list = document.getElementById('place_types');
    let place_list_div = document.getElementsByClassName('tripBriefInfoList')[0];
    let place_list =  place_list_div.getElementsByTagName('ul')[0];
    place_list.innerHTML = '';

    place_types_list.innerHTML = '';
    let trip_places = the_plan.trip_places;
    let place_type_array = [... new Set( trip_places.map((x) => x.place_type) )];

    place_type_array.forEach(place_type => {
        let place_type_item = elementFromHTML(` <li>
                                                    <div class="placeType text-center">
                                                        ${place_type.replace("_", " ")}
                                                    </div>
                                                </li>`);
        place_types_list.appendChild(place_type_item);
    });

    trip_places.forEach((trip_place) => {
        let trip_place_item = elementFromHTML(`<li class="list-group-item">        
                                                    <div class="tripBriefInfo">
                                                        <p>${trip_place.name || 'Noname'}</p>
                                                    </div>  
                                                    <div class="tripBriefInfo">
                                                        <p>${trip_place.place_type}</p>
                                                    </div>  
                                                    <div class="tripBriefInfo">
                                                        <a href="${trip_place.google_maps_url}">View In Map</a>
                                                    </div>
                                                </li>`);
        place_list.appendChild(trip_place_item);
    });

    document.getElementById('operateTripPlan').addEventListener('click', function () {

        if (inRecommenderPage) {
            
            request_settings.data = JSON.stringify({ host_id: the_plan.host_infos.id, 
                                                        start_date: the_plan.start_date,
                                                        end_date: the_plan.end_date,
                                                        place_id_list: trip_places.map((x) => x.id)});  
            
            request_settings.url = "http://localhost:8000/trip_plans/add-plan-to-calender";
            request_settings.method = "POST";
    
            planDetailModal.hide();
            $.ajax(request_settings).done(function (_) {
    
                setTimeout(() => {
                    const sideNotification = document.getElementById('sideNotification');
                    const sideNotificationBody = document.getElementById('sideNotificationBody');
                    sideNotificationBody.innerText = "Plan added successfully!";
                    const sideNotificationInstance = new bootstrap.Toast(sideNotification);
                    sideNotificationInstance.show();
                    setTimeout(() => window.location.assign('http://localhost:8000/personal_info/calender') , 3000);
                }, 2000);
                window.scrollTo(0, 0);
            }).fail(function (errorobj, textstatus, error) {
                document.getElementById('popup-warning').getElementsByClassName('alertBox')[0].children[1].innerHTML = JSON.stringify(error)
                popupWarningModal.show()
                // setTimeout(() => {
                //     const sideNotification = document.getElementById('sideNotification');
                //     const sideNotificationBody = document.getElementById('sideNotificationBody');
                //     sideNotificationBody.innerText = "Cannot added plan!";
                //     const sideNotificationInstance = new bootstrap.Toast(sideNotification);
                //     sideNotificationInstance.show();
                // }, 2000);
            });

        } else {
            request_settings.url = `http://localhost:8000/trip_plans/remove-plan-from-calender/${planId}/`;
            request_settings.method = "DELETE";
    
            planDetailModal.hide();
            $.ajax(request_settings).done(function (_) {
    
                setTimeout(() => {
                    const sideNotification = document.getElementById('sideNotification');
                    const sideNotificationBody = document.getElementById('sideNotificationBody');
                    sideNotificationBody.innerText = "Plan deleted successfully!";
                    const sideNotificationInstance = new bootstrap.Toast(sideNotification);
                    sideNotificationInstance.show();
                    setTimeout(() => window.location.assign('http://localhost:8000/personal_info/calender') , 3000);
                }, 2000);
                plan_list = plan_list.slice(0, indexOfPlan).concat(plan_list.slice(indexOfPlan+1));
                event_list = event_list.findIndex((x) =>  x.id === planId);
                setupCalender();
            });
        }
        
    });
}

function setPlanRate(planId) {
    
    rangeInput = document.getElementById("rateButton");

    rangeInput.addEventListener("change", function() {

        request_settings.url = "http://localhost:8000/trip_plans/set-rate";
        request_settings.method = "POST";
        request_settings.data = JSON.stringify({
            "plan_id": planId,
            "rate_score": rangeInput.value
        });
        
        $.ajax(request_settings).done(function (response) {
            console.log(response);
        });
    }, false);

}
