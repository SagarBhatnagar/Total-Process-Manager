document.getElementById('gtin').addEventListener('blur', validateGTIN);

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