
var last_reviewed_host_list = [];
var last_reviewed_host_offset = 0;
var total_pages_reviewed_host = 0;
var last_reviewed_trip_plan_list = [];
var last_reviewed_trip_plan_offset = 0;
var total_pages_reviewed_trip_plan = 0;


request_settings.method = "GET"
request_settings.url = "http://localhost:8000/host_info/get-all-rates"

$.ajax(request_settings).done(function (response) {
    last_reviewed_host_list = response.all_host_rates;
    total_pages_reviewed_host =  Math.ceil(last_reviewed_host_list.length / 10);
    var aTag , liTag;
    let paginationPages = document.getElementById('recentVisitedHosts')
                                        .getElementsByClassName('pagination')[0]
    for (let index = 1; index <= total_pages_reviewed_host; index++) {
        aTag = document.createElement("a");
        aTag.className = "page-link";
        aTag.href = '#';
        aTag.innerText = index.toString();
        liTag = document.createElement("li");
        liTag.className = "page-item";
        liTag.appendChild(aTag);
        paginationPages.insertBefore(liTag, 
                    paginationPages.getElementsByClassName('next')[0]);
    }
    last_reviewed_host_offset = 1;
    rebuildTable(last_reviewed_host_list, 
                    'recentVisitedHosts'
                    ,last_reviewed_host_offset
                    ,total_pages_reviewed_host);
});

request_settings.url = "http://localhost:8000/trip_plans/get-all-rates"

$.ajax(request_settings).done(function (response) {
    last_reviewed_trip_plan_list = response.all_trip_plan_rates
                                             last_reviewed_host_list = response.all_host_rates;
    total_pages_reviewed_trip_plan =  Math.ceil(last_reviewed_trip_plan_list.length / 10);
    var aTag , liTag;
    let paginationPages = document.getElementById('recentVisitedTripPlans')
                                        .getElementsByClassName('pagination')[0]
    for (let index = 1; index <= total_pages_reviewed_trip_plan; index++) {
        aTag = document.createElement("a");
        aTag.className = "page-link";
        aTag.href = '#';
        aTag.innerText = index.toString();
        liTag = document.createElement("li");
        liTag.className = "page-item";
        liTag.appendChild(aTag);
        paginationPages.insertBefore(liTag, 
                    paginationPages.getElementsByClassName('next')[0]);
    }
    last_reviewed_trip_plan_offset = 1;
    rebuildTable(last_reviewed_trip_plan_list, 
                    'recentVisitedTripPlans'
                    ,last_reviewed_trip_plan_offset
                    ,total_pages_reviewed_trip_plan);
});

$(document).on("click", ".page-item", (event) => {
    let tableId = ''
    let rate_list = [];
    if (event.target.parentNode.parentNode.parentNode.id.includes('Host')) {
        tableId = 'recentVisitedHosts'; 
        rate_list = last_reviewed_host_list;
    } else {
        tableId = 'recentVisitedTripPlans';
        rate_list = last_reviewed_trip_plan_list;
    }
    if (event.target.parentNode.className.includes('previous')) {
        last_reviewed_host_offset = last_reviewed_host_offset - 1;
    } else if (event.target.parentNode.className.includes('next')){
        last_reviewed_host_offset = last_reviewed_host_offset + 1;
    }
    else {
        let listNode = event.target.parentNode.parentNode;
        last_reviewed_host_offset = 
                Array.prototype.slice.call(listNode.children)
                    .indexOf(event.target.parentNode);
    }
    rebuildTable(rate_list, tableId, 
                    last_reviewed_host_offset,
                    total_pages_reviewed_host);
});

function rebuildTable(rate_list = [], tableContainerId, pageNo, lastPage) {
    let paginationPages = document.getElementById(tableContainerId).getElementsByClassName('pagination')[0];
    let pages = [...paginationPages.getElementsByClassName('page-link')];
    for (let index = 1; index <= lastPage; index++) {
        if(index === pageNo){
            pages[index].innerHTML = `<strong>${pageNo}</strong>`;
        }
        else{
            pages[index].innerText = index.toString();
        }
    }
    if(pageNo === 1){
        paginationPages.getElementsByClassName('previous')[0].hidden = true;
        paginationPages.getElementsByClassName('next')[0].hidden = lastPage === 1 ? true : false;
    }
    else if(pageNo === lastPage){
        paginationPages.getElementsByClassName('previous')[0].hidden = false;
        paginationPages.getElementsByClassName('next')[0].hidden = true;
    }
    else {
        paginationPages.getElementsByClassName('previous')[0].hidden = false;
        paginationPages.getElementsByClassName('next')[0].hidden = false;
    }
    let tableBody = document.getElementById(tableContainerId).getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
    let row, newTh, newTr;
    for (let index = (pageNo - 1) * 10; index < (pageNo) * 10 && index < rate_list.length; index++) {
        row = rate_list[index];
        newTr = document.createElement('tr');
        newTh = document.createElement('th');
        newTh.innerText = row.id;
        newTr.appendChild(newTh);
        newTh = document.createElement('th');
        newTh.innerText = row.name;
        newTr.appendChild(newTh);
        newTh = document.createElement('th');
        newTh.innerText = row.rate_score;
        newTr.appendChild(newTh);
        newTr.className = tableContainerId.includes('Host') ? "table-primary": "table-success";
        tableBody.appendChild(newTr);
    }
    // if(10 > tableBody.children.length){
    //     for (let index2 = tableBody.children.length; index2 < 10; index2++) {
    //         newTr = document.createElement('tr');
    //         let i = 0;
    //         while (i < 3) {
    //             newTh = document.createElement('th');
    //             newTh.innerText = "test";
    //             newTh.className = "table-primary";
    //             newTr.appendChild(newTh);
    //             i++;
    //         }
    //         newTr.className = "table-primary";
    //         tableBody.appendChild(newTr);
    //     }
    // }
}

