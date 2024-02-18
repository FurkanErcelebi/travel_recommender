
var personalInfoEditModal = new bootstrap.Modal(document.getElementById('personalInfoEditModal'))

let survey_response = {survey_infos: []};

request_settings.url = "http://localhost:8000/personal_info/get-survey-responses";
request_settings.method = "GET";

function set_survey_values(survey_info) {
    let survey_info_div = document.getElementById(survey_info.div_id);
    survey_info.keys_and_values.forEach(keys_and_value => {
        let survey_field = survey_info_div.querySelector("#" + keys_and_value.key);
        let survey_value = survey_field.getElementsByClassName("surveyValue");
        survey_value.item(0).childNodes[1].innerHTML = keys_and_value.label || keys_and_value.value;
    });
}

$.ajax(request_settings).done(function (response) {
    survey_response = response;
    survey_response.survey_infos.forEach(survey_info => set_survey_values(survey_info));
});

var submit_button_list = document.getElementsByClassName('submitButton');

for (const submit_button of submit_button_list) {
    submit_button.parentElement.parentElement.hidden = true;
}


var collapseElementList = [].slice.call(document.querySelectorAll('.collapse'))
collapseElementList = collapseElementList.slice(1);

var survey_open_buttons = document.querySelectorAll('button[class^="openSurvey"]')
var survey_edit_forms = document.getElementsByClassName("modal-body");
survey_edit_forms = survey_edit_forms[0].childNodes[1].children;

for (const survey_open_button of survey_open_buttons) {
    survey_open_button.addEventListener('click', () => {
        for (const collapseElement of collapseElementList) {
            
            if (collapseElement.id === survey_open_button.id.substring(7)) {
                new bootstrap.Collapse(collapseElement);
            }
            else{
                if(collapseElement.className.includes('show')){
                    new bootstrap.Collapse(collapseElement);
                }
            }

        }

        new Promise(r => setTimeout(r, 2000));
    });
}

new bootstrap.Collapse(collapseElementList[0]);

let editButton = document.getElementById("editButton");
//editButton.innerHTML = "Edit Survey";

let selected_edit_form = null;

editButton.addEventListener("click", () => {
    personalInfoEditModal.show()
    let showed_survey = collapseElementList.filter((collapseElement) => {
        return collapseElement.className.includes("show");
    });

    selected_edit_form = null;
    for (const survey_edit_form of survey_edit_forms) {
        if("edit_" + showed_survey[0].id === survey_edit_form.id ){
            survey_edit_form.hidden = false;
            selected_edit_form = survey_edit_form
        }
        else {
            survey_edit_form.hidden = true;
        }
    }

    if(selected_edit_form !== null){

        selected_survey_infos = survey_response.survey_infos.filter((infos) => { return selected_edit_form.id.substring(5) === infos.div_id})[0]
        let response_fields = [].slice.call(
            selected_edit_form.getElementsByTagName("td")).filter((field_response) => 
                    {
                        return field_response.childNodes[1] !== undefined ? 
                            field_response.childNodes[1].className.startsWith("survey-response") : false;
                    });

        response_fields.forEach((form_field => {
            if(form_field.childNodes[1].className.endsWith('number') 
                    || form_field.childNodes[1].className.endsWith('range')
                    || form_field.childNodes[1].className.endsWith('select')){
                
                field_value = selected_survey_infos.keys_and_values.filter((selected_survey_info) => { 
                                    return selected_survey_info.key === form_field.parentElement
                                                                                .getElementsByTagName("label")[0]
                                                                                .getAttribute('for').substring(3)
                                })[0].value;
                
                form_field.childNodes[1].childNodes[1].value = field_value;

            }
            else if(form_field.childNodes[1].className.endsWith('radio')
                    || form_field.childNodes[1].className.endsWith('checkbox')) {
                
                field_values = selected_survey_infos.keys_and_values.filter((selected_survey_info) => { 
                        return selected_survey_info.key === form_field.parentElement
                                                                .getElementsByTagName("label")[0]
                                                                .getAttribute("id")
                        })[0].value;
                
                [].slice.call(field_values).forEach((field_value) => {
                    [].slice.call(form_field.getElementsByClassName('form-check'))[field_value - 1].childNodes[1].checked = true;
                });

            }

        }))
    }

})

var save_new_personal_info = document.getElementsByClassName("saveNewPersonalInfo")[0];

save_new_personal_info.addEventListener('click', () => {

    if(selected_edit_form !== null){
        
        var firstErrorField = null;
        let error_fields = [...document.querySelectorAll('div[class^="survey"]')].filter((element) => {
            let survey_id = element.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id.substring(5)   
            return element.className.includes("ErrorMsg") && survey_id === selected_survey_infos.div_id
        });

        for (let error_field of error_fields) {
            if(error_field.innerHTML.replace("\n","").trim().length > 0){
                if(firstErrorField == null){
                    firstErrorField = error_field;
                }
            }
        }

        if(firstErrorField === null){
            valid = true;
        }

        if(valid){

            let response_fields = [].slice.call(
                selected_edit_form.getElementsByTagName("td")).filter((field_response) => 
                        {
                            return field_response.childNodes[1] !== undefined ? 
                                field_response.childNodes[1].className.startsWith("survey-response") : false;
                        });
            
            let label_field_and_values = {}
            response_fields.forEach((form_field => {
    
                let className = form_field.childNodes[1].className
                if(className.endsWith('number')
                    || className.endsWith('range')
                    || className.endsWith('select')){
                    
                    let form_key = form_field.parentElement
                                            .getElementsByTagName("label")[0]
                                            .getAttribute('for').substring(3);
                    
                    selected_survey_infos.keys_and_values.forEach((selected_survey_info) => { 
                        let value_node = form_field.childNodes[1].childNodes[1];
                        if(selected_survey_info.key === form_key ) {
                            selected_survey_info.value = parseInt(value_node.value);
                            if(className.endsWith('select')){
                                let selectedIndex = value_node.selectedIndex;
                                label_field_and_values[form_key] = value_node[selectedIndex].text;
                            }
                        }
                    });
                    
    
                }
                else if(className.endsWith('radio')
                        || className.endsWith('checkbox')) {
                    
                    var form_check_list = [].slice.call(form_field.getElementsByClassName('form-check'));
                    
                    let value_list = [];
                    let label_list = []
                    for (let index = 0; index < form_check_list.length; index++) {
                        if(form_check_list[index].childNodes[1].checked){
                            let checkChild = form_check_list[index].childNodes;
                            let start_id = checkChild[1].id.lastIndexOf("_");
                            value = parseInt(checkChild[1].id.substring(start_id + 1)) + 1;
                            value_list.push(value);
                            label_list.push(checkChild[3].innerText)
                        }
                        
                    }
    
                    let form_key = form_field.parentElement
                                            .getElementsByTagName("label")[0]
                                            .getAttribute('id');
    
                    selected_survey_infos.keys_and_values.forEach((selected_survey_info) => { 
                        if(selected_survey_info.key === form_key ) {
                            selected_survey_info.value = value_list.length == 1 ? value_list[0] : value_list;
                            label_field_and_values[form_key] = label_list
                        }
                    });
    
                }
                
    
            }));

            console.log(selected_survey_infos);

            request_settings.url = "http://localhost:8000/personal_info/new-survey-responses";
            request_settings.method = "POST";
            request_settings.data = JSON.stringify(selected_survey_infos);
                
            $.ajax(request_settings).done(function (response) {
                survey_response = response['message'];
                
                if(survey_response.startsWith("Success")){
                    let alert = document.getElementsByClassName("alert-success")[0];
                    alert.childNodes[1].innerHTML = survey_response
                    new bootstrap.Alert(alert);
                    new Promise(r => setTimeout(r, 2000));
                    // alert.closest();
                    Object.entries(label_field_and_values).forEach((label_field_and_value) => {
                        selected_survey_infos.keys_and_values.find((x) => x.key === label_field_and_value[0]).label = label_field_and_value[1];
                    });
                    set_survey_values(selected_survey_infos);
                }
                else{
                    let alert = document.getElementsByClassName("alert-warning")[0];
                    alert.childNodes[1].innerHTML = survey_response
                    new bootstrap.Alert(alert);
                    new Promise(r => setTimeout(r, 2000));
                    // alert.closest();
                }
                personalInfoEditModal.hide();
            
            });

            console.log("Submit new survey");
        }
        else{
            firstErrorField.scrollIntoView();
            console.log("Submit error");
        }
    }

});


