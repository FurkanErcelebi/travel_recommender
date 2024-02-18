let valid = false;

function isRadioOrCheckbox(element) {
    
    return element.className.endsWith('radio') || element.className.endsWith('checkbox')

}

let all_elements = [...document.querySelectorAll('div[class^="personal_field"]')];

function controlFields(elements) {
    
    let id = elements.childNodes[1].id;
    let rawValue = elements.childNodes[1].value;
    let i = 0;
    if (rawValue === '') {
        valid = false;
        addErrorMessage('please enter info', 'infoErrorMsg', 0, 0, id, id + '1');
    }
    else{
        removeErrorMessage(id ,id + '1');
        i++;
    }

    if(rawValue.length < 5){
        valid = false;
        addErrorMessage('less than 5', 'infoErrorMsg', 0, 0, id, id + '2');
    }
    else{
        removeErrorMessage(id ,id + '2');
        i++;
    }

    if(id === 'id_cell_phone_no'){

        const myRe = /^[0-9]{3}-[0-9]{3}-[0-9]{2}-[0-9]{2}$/gm;
        const array = myRe.exec(rawValue);
        if (array === null) {
            valid = false;
            addErrorMessage('follow phone number rule', 'infoErrorMsg', 0, 0, id, id + '1');
        }
        else{
            removeErrorMessage(id ,id + '1');
            i++;
        }

    }
    else{
        i++;
    }

    if(i == 3){
        valid = true;
    }
    

}

for (const elements of all_elements) {
    elements.addEventListener("input", () => {controlFields(elements)});  
}



$("#save-survey").click(function() {

    
    for (const elements of all_elements) {
        controlFields(elements);  
    }
    
    if(valid){
      $("#survey-form").submit();
    }
    else{
        console.log("not valid form");   
    }
    
});