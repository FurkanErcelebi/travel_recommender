
let valid = false;

function isRadioOrCheckbox(element) {
    
    return element.className.endsWith('radio') || element.className.endsWith('checkbox')

}


let all_elements = [...document.querySelectorAll('div[class^="survey-response-for-"]')];
let range_elements = document.getElementsByClassName("survey-response-for-range");
let select_elements = document.getElementsByClassName("survey-response-for-select");

let single_elements = all_elements.filter(elm => !isRadioOrCheckbox(elm)
                                 && !elm.className.endsWith('range') && !elm.className.endsWith('select'));

let multi_elements = all_elements .filter(elm => isRadioOrCheckbox(elm)
                                 && !elm.className.endsWith('range') && !elm.className.endsWith('select'));

function controlNumberField(fieldValue) {
    
    if(fieldValue === undefined){
        return false;
    }
    for (let index = 1; index < fieldValue.length; index++) {

        if(fieldValue[index] !== '0' &&
            fieldValue[index] !== '1' &&
            fieldValue[index] !== '2' &&
            fieldValue[index] !== '3' &&
            fieldValue[index] !== '4' &&
            fieldValue[index] !== '5' &&
            fieldValue[index] !== '6' &&
            fieldValue[index] !== '7' &&
            fieldValue[index] !== '8' &&
            fieldValue[index] !== '9' ){
                return false;
        }
        
    }

    return true;

}

function controlNumberFields(elements) {
    
    let id = elements.childNodes[1].id;
    let rawValue = elements.childNodes[1].value;
    if(controlNumberField(rawValue)){

        removeErrorMessage(id ,id + '4');
        let i = 0;
        let value = parseInt(rawValue);
        if (value > 100) {
            valid = false;
            addErrorMessage('value must be less than 100', 'surveyErrorMsg', 0, 0, id, id + '1');
        }
        else{
            removeErrorMessage(id ,id + '1');
            i++;
        }
        if (value < 0){
            valid = false;
            addErrorMessage('value must be positive', 'surveyErrorMsg', 0, 0, id, id + '2');
        }
        else{
            removeErrorMessage(id ,id + '2');
            i++;
        }
        if (isNaN(value)) {
            valid = false;
            addErrorMessage('please give positive value', 'surveyErrorMsg', 0, 0, id, id + '3');
        }
        else{
            removeErrorMessage(id ,id + '3');
            i++;
        }
        if(i == 3){
            value = 3;
        }
    }
    else {
        valid = false;
        addErrorMessage('give sign only value', 'surveyErrorMsg', 0, 0, id, id + '4');
    }

}

for (const elements of single_elements) {
    elements.addEventListener("input", () => {controlNumberFields(elements)});  
}

for (const elements of select_elements) {
    elements.addEventListener("change", () => {
        let select_elm = elements.childNodes[1];
        let id = select_elm.id;
        if(select_elm.value === '0'){
            valid = false;
            addErrorMessage('please select one of theme', 'surveyErrorMsg', 0, 0, id, id + '1');
        }
        else{
            valid = true;
            removeErrorMessage(id ,id + '1');
        }
    });  
}


for (const elements of range_elements) {
    let child = elements.childNodes[1];
    document.getElementById(child.id + '_value').innerHTML = child.value;;
    elements.addEventListener("input", (e) => {
        document.getElementById(e.target.id + '_value').innerHTML = e.target.value;
    });  
}


i = 0;
for (const elements of multi_elements) {

    for (const radioDiv of elements.getElementsByClassName("form-check")){
        radioDiv.childNodes[1].onclick = function() {
            let id = radioDiv.childNodes[1].id;
            let errorId = id.substring(0, id.lastIndexOf('_')) + '_error';
            removeErrorMessage(null, errorId);
        }
    }
    i++;

}


$("#save-survey").click(function() {
    
    if(location.pathname.startsWith('/surveys')){

        if ($('input[type=radio]:checked').length > 0) {
            valid = true; 
        }
    
        if ($('input[type=checkbox]:checked').length > 0) {
            valid = true; 
        }
        
    }

    if(valid){
      $("#survey-form").submit();
    }
    else{
        
        for (const elements of single_elements) {
            controlNumberFields(elements);  
        }

        for (const elements of select_elements) {
            let select_elm = elements.childNodes[1];
            if(select_elm.value === '0'){
                addErrorMessage('please select one of them', 'surveyErrorMsg', 0, 0, select_elm.id, select_elm.id + '1');
            }  
        }
        
        i = 0;
        for (const elements of multi_elements) {

            let cnt = 0;
            let radioDivs = elements.getElementsByClassName("form-check");
            for (const radioDiv of radioDivs){
                if(radioDiv.childNodes[0].checked){
                    cnt++;
                }
            }

            if(cnt == 0){
                let id = radioDivs[0].childNodes[1].id;
                let errorId = id.substring(0, id.lastIndexOf('_')) + '_error';
                addErrorMessage('please click one of the options',
                            'survey_'+ elements.className.substring(20) +'ErrorMsg', 3, 0, id, errorId, false);
            }

            i++;
        }

        console.log("not valid form");
    }
});