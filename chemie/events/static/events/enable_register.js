//Enables register button if events TOS is accepted

let tos = document.getElementById('id_approval');
let btn = document.getElementById('register_or_edit');

$(document.getElementById('id_approval')).change(
    function() {
        btn.disabled = !tos.checked;
    });
