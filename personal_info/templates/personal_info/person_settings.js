
var personalInfoEditModal = new bootstrap.Modal(document.getElementById('personalInfoEditModal'));

let settings_info_details = {};


let settings_infos = [...document.getElementsByClassName('settingsPersonInfos')[0].getElementsByTagName('li')];

for (let settings_info of settings_infos){
    let settingChildren = settings_info.children;
    settings_info_details[settingChildren[0].id] = settingChildren[1].innerText;
}



document.getElementsByClassName('submitButton')[0].parentElement.parentElement.hidden = true;

let editButton = document.getElementById("editButton");

editButton.addEventListener("click", () => {
    
    personalInfoEditModal.show()
    for(let personal_field of all_elements){
        if (settings_info_details[personal_field.children[0].name]) {
            personal_field.children[0].value = settings_info_details[personal_field.children[0].name];
        }
    }

});

var save_new_personal_info = document.getElementsByClassName("saveNewPersonalInfo")[0];

save_new_personal_info.addEventListener('click', () => {

    for (const elements of all_elements) {
        controlFields(elements);  
    }

    if(valid){

        for(let personal_field of all_elements){
            if (settings_info_details[personal_field.children[0].name]) {
                settings_info_details[personal_field.children[0].name] = personal_field.children[0].value;
            }
        }
        
        request_settings.url = "http://localhost:8000/personal_info/new-personal-info"
        request_settings.method = "POST"
        request_settings.data = JSON.stringify(settings_info_details)

        $.ajax(request_settings).done(function (response) {
            personal_info_response = response['message'];
            
            if(personal_info_response.startsWith("Success")){
                let alert = document.getElementsByClassName("alert-success")[0];
                alert.childNodes[1].innerHTML = personal_info_response
                new bootstrap.Alert(alert);
                new Promise(r => setTimeout(r, 2000));
                // alert.closest();
                Object.entries(settings_info_details).forEach((key_and_value)=> {
                    let founded_info = settings_infos.find((x) => x.children[0].id === key_and_value[0])
                    if(founded_info){
                        founded_info.children[1].innerText = key_and_value[1];
                    }
                });
            }
            else{
                let alert = document.getElementsByClassName("alert-warning")[0];
                alert.childNodes[1].innerHTML = personal_info_response
                new bootstrap.Alert(alert);
                new Promise(r => setTimeout(r, 2000));
                // alert.closest();
            }
            personalInfoEditModal.hide();
                        
        });

    }

    
//     if(selected_edit_form !== null){
        
//         var firstErrorField = null;
//         let error_fields = [...document.querySelectorAll('div[class^="survey"]')].filter((element) => {
//             let survey_id = element.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id.substring(5)   
//             return element.className.includes("ErrorMsg") && survey_id === selected_survey_infos.div_id
//         });

//         for (let error_field of error_fields) {
//             if(error_field.innerHTML.replace("\n","").trim().length > 0){
//                 if(firstErrorField == null){
//                     firstErrorField = error_field;
//                 }
//             }
//         }

//         if(firstErrorField === null){
//             valid = true;
//         }

//         if(valid){

//             let response_fields = [].slice.call(
//                 selected_edit_form.getElementsByTagName("td")).filter((field_response) => 
//                         {
//                             return field_response.childNodes[1] !== undefined ? 
//                                 field_response.childNodes[1].className.startsWith("survey-response") : false;
//                         });
            
//             let label_field_and_values = {}
//             response_fields.forEach((form_field => {
    
//                 let className = form_field.childNodes[1].className
//                 if(className.endsWith('number')
//                     || className.endsWith('range')
//                     || className.endsWith('select')){
                    
//                     let form_key = form_field.parentElement
//                                             .getElementsByTagName("label")[0]
//                                             .getAttribute('for').substring(3);
                    
//                     selected_survey_infos.keys_and_values.forEach((selected_survey_info) => { 
//                         let value_node = form_field.childNodes[1].childNodes[1];
//                         if(selected_survey_info.key === form_key ) {
//                             selected_survey_info.value = parseInt(value_node.value);
//                             if(className.endsWith('select')){
//                                 let selectedIndex = value_node.selectedIndex;
//                                 label_field_and_values[form_key] = value_node[selectedIndex].text;
//                             }
//                         }
//                     });
                    
    
//                 }
//                 else if(className.endsWith('radio')
//                         || className.endsWith('checkbox')) {
                    
//                     var form_check_list = [].slice.call(form_field.getElementsByClassName('form-check'));
                    
//                     let value_list = [];
//                     let label_list = []
//                     for (let index = 0; index < form_check_list.length; index++) {
//                         if(form_check_list[index].childNodes[1].checked){
//                             let checkChild = form_check_list[index].childNodes;
//                             let start_id = checkChild[1].id.lastIndexOf("_");
//                             value = parseInt(checkChild[1].id.substring(start_id + 1)) + 1;
//                             value_list.push(value);
//                             label_list.push(checkChild[3].innerText)
//                         }
                        
//                     }
    
//                     let form_key = form_field.parentElement
//                                             .getElementsByTagName("label")[0]
//                                             .getAttribute('id');
    
//                     selected_survey_infos.keys_and_values.forEach((selected_survey_info) => { 
//                         if(selected_survey_info.key === form_key ) {
//                             selected_survey_info.value = value_list.length == 1 ? value_list[0] : value_list;
//                             label_field_and_values[form_key] = label_list
//                         }
//                     });
    
//                 }
                
    
//             }));

//             console.log(selected_survey_infos);

//             var settings = {
//                 "url": "http://localhost:8000/personal_info/new-survey-responses",
//                 "method": "POST",
//                 "timeout": 0,
//                 "headers": {
//                     "Content-Type": "application/json"
//                 },
//                 "data" : JSON.stringify(selected_survey_infos)
//                 };
                
//             $.ajax(settings).done(function (response) {
//                 survey_response = response['message'];
                
//                 if(survey_response.startsWith("Success")){
//                     let alert = document.getElementsByClassName("alert-success")[0];
//                     alert.childNodes[1].innerHTML = survey_response
//                     new bootstrap.Alert(alert);
//                     new Promise(r => setTimeout(r, 2000));
//                     // alert.closest();
//                     Object.entries(label_field_and_values).forEach((label_field_and_value) => {
//                         selected_survey_infos.keys_and_values.find((x) => x.key === label_field_and_value[0]).label = label_field_and_value[1];
//                     });
//                     set_survey_values(selected_survey_infos);
//                 }
//                 else{
//                     let alert = document.getElementsByClassName("alert-warning")[0];
//                     alert.childNodes[1].innerHTML = survey_response
//                     new bootstrap.Alert(alert);
//                     new Promise(r => setTimeout(r, 2000));
//                     // alert.closest();
//                 }
//                 personalInfoEditModal.hide();
            
//             });

//             console.log("Submit new survey");
//         }
//         else{
//             firstErrorField.scrollIntoView();
//             console.log("Submit error");
//         }
//     }

});


