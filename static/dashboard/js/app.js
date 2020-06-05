function shuffleButtonDisabler() {
    let button = document.getElementById('shuffleButton');
    button.disabled = false;
}

$(document).ready(function() {
     setTimeout(function() {
        $("#alert").alert('close');
    }, 5000);
});
