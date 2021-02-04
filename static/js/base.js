function onResize(){
    if ($('#topBar h1').height() > 100){
        $('#nav_side .sidebar').sidebar('hide', );
        $('#sidebar_button').show();
    }
    else {
        $('#nav_side .sidebar').sidebar('show');
        $('#sidebar_button').hide();
    }
}

$(document).ready(function(){
    onResize();
})

function showAlert(alert, message){
    $('h1', alert).html(message);
    alert.removeClass('hidden');
    setTimeout(function(){
        alert.addClass('hidden');
    }, 2500);
}

function showSuccess(message){
    showAlert($('#alert-success'), message);
}

function showInfo(message){
    showAlert($('#alert-info'), message);
}

function showError(message){
    showAlert($('#alert-error'), message);
}

$(document).ready(function(){
    $('.alert .close.icon').click(function(e){
        $(e.target.parentElement).addClass('hidden');
    });
})