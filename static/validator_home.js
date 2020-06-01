document.getElementById('gtin').addEventListener('blur', validateGTIN);
document.getElementById('project_manager').addEventListener('blur', validatePM)
document.getElementById('reviewer').addEventListener('blur', validateR)

function validateGTIN(){
    const gtin = document.getElementById('gtin');
    const re = /^\d{14}$/;

    if(!re.test(gtin.value)){
        gtin.classList.add('is-invalid');
        document.getElementById('vgtin').style.display = 'block'
    }
    else{
        gtin.classList.remove('is-invalid');
        gtin.classList.add('is-valid');
        document.getElementById('vgtin').style.display = 'none'
    }
}

function validatePM(){
    const project_manager = document.getElementById('project_manager');
    const re = /^[a-zA-Z ]+$/;

    if(!re.test(project_manager.value)){
        project_manager.classList.add('is-invalid');
    }
    else{
        project_manager.classList.remove('is-invalid');
        project_manager.classList.add('is-valid');

    }
}

function validateR(){
    const reviewer = document.getElementById('reviewer');
    const re = /^[a-zA-Z ]+$/;

    if(!re.test(reviewer.value)){
        reviewer.classList.add('is-invalid');
    }
    else{
        reviewer.classList.remove('is-invalid');
        reviewer.classList.add('is-valid');        
    }
}