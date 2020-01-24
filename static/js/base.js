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