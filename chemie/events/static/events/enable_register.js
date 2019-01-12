//Enables register button if event TOS is accepted

function enableRegister(){
    let tos = document.getElementById('tos');
    document.getElementById('register_or_edit').disabled = !tos.checked;
}
