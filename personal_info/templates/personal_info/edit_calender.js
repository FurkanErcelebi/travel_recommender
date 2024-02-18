
var planDetailModal = new bootstrap.Modal(document.getElementById('planDetailModal'));

var calendar = undefined
let plan_list = []
let event_list = []

$(document).ready(function() {

    let editCalender = document.getElementById("editButton");
    
    editCalender.addEventListener("click", () => {
        window.location.assign("http://localhost:8000/rcm_plans");
    });

    // remove when submit
    $('#external-events div.external-event').each(function() {
		
        // create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
        // it doesn't need to have a start or end
        var eventObject = {
            title: $.trim($(this).text()) // use the element's text as the event title
        };
        
        // store the Event Object in the DOM element so we can get to it later
        $(this).data('eventObject', eventObject);
        
        // make the event draggable using jQuery UI
        $(this).draggable({
            zIndex: 999,
            revert: true,      // will cause the event to go back to its
            revertDuration: 0  //  original position after the drag
        });
        
    });
    // remove when submit

    request_settings.url = "http://localhost:8000/trip_plans/get-plans";
    request_settings.method = "GET";

    $.ajax(request_settings).done(function (response) {
            plan_list = response.trip_plans;
            plan_list.forEach((the_plan) => {
                let start_dates = the_plan.start_date.split('-');
                let end_dates = the_plan.end_date.split('-');
                event_list.push({
                    id: the_plan.id,
                    title: `Go trip to  ${the_plan.host_infos.name}`,
                    start: new Date(start_dates[0], start_dates[1] - 1, start_dates[2]),
                    end: new Date(end_dates[0], end_dates[1] - 1, end_dates[2]),
                    className: 'success'
                });
            });

            setupCalender();
        });  
});

$(document).on("click", "span.fc-event-title", (event) => {
    console.log(event.target);
    let planId = parseInt(event.target.classList[1].split('-')[2]);
    let planIndex = plan_list.findIndex((x) => x.id === planId);
    operateOnPlan(planIndex);
});

function setupCalender() {
        
    // remove when submit
    calendar =  $('#calendar').fullCalendar({
        header: {
            left: 'title',
            center: 'agendaDay,agendaWeek,month',
            right: 'prev,next today'
        },
        editable: true,
        firstDay: 1, //  1(Monday) this can be changed to 0(Sunday) for the USA system
        selectable: true,
        defaultView: 'month',
        
        axisFormat: 'h:mm',
        columnFormat: {
            month: 'ddd',    // Mon
            week: 'ddd d', // Mon 7
            day: 'dddd M/d',  // Monday 9/7
            agendaDay: 'dddd d'
        },
        titleFormat: {
            month: 'MMMM yyyy', // September 2009
            week: "MMMM yyyy", // September 2009
            day: 'MMMM yyyy'                  // Tuesday, Sep 8, 2009
        },
        allDaySlot: false,
        selectHelper: true,
        select: function(start, end, allDay) {
            var title = prompt('Event Title:');
            if (title) {
                calendar.fullCalendar('renderEvent',
                    {
                        title: title,
                        start: start,
                        end: end,
                        allDay: allDay
                    },
                    true // make the event "stick"
                );
            }
            calendar.fullCalendar('unselect');
        },
        droppable: true, // this allows things to be dropped onto the calendar !!!
        drop: function(date, allDay) { // this function is called when something is dropped
        
            // retrieve the dropped element's stored Event Object
            var originalEventObject = $(this).data('eventObject');
            
            // we need to copy it, so that multiple events don't have a reference to the same object
            var copiedEventObject = $.extend({}, originalEventObject);
            
            // assign it the date that was reported
            copiedEventObject.start = date;
            copiedEventObject.allDay = allDay;
            
            // render the event on the calendar
            // the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
            $('#calendar').fullCalendar('renderEvent', copiedEventObject, true);
            
            // is the "remove after drop" checkbox checked?
            if ($('#drop-remove').is(':checked')) {
                // if so, remove the element from the "Draggable Events" list
                $(this).remove();
            }
            
        },
        
        events: event_list
        
        
    });
    // remove when submit
}
