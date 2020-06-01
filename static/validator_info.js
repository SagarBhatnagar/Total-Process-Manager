document.getElementById('project_manager').addEventListener('blur', validatePM)
document.getElementById('project_lead').addEventListener('blur', validatePL)
document.getElementById('reviewer').addEventListener('blur', validateR)
document.getElementById('assigned_to').addEventListener('blur', validateAT)

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


function validatePL(){
    const project_lead = document.getElementById('project_lead');
    const re = /^[a-zA-Z ]+$/;

    if(!re.test(project_lead.value)){
        project_lead.classList.add('is-invalid');
    }
    else{
        project_lead.classList.remove('is-invalid');
        project_lead.classList.add('is-valid');

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

function validateAT(){
    const reviewer = document.getElementById('assigned_to');
    const re = /^[a-zA-Z ]+$/;

    if(!re.test(assigned_to.value)){
        assigned_to.classList.add('is-invalid');
    }
    else{
        assigned_to.classList.remove('is-invalid');
        assigned_to.classList.add('is-valid');

    }
}