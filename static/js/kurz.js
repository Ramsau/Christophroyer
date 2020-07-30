function updateCharCount() {
    $('#chars_remaining').html(255 - $('#kurz_text').val().length);
}

let kurz_submitUrl;
let kurz_csrftoken;
function submitText(text) {
    $.ajax({
        url: kurz_submitUrl,
        method: 'POST',
        data: {
            text: text,
            csrfmiddlewaretoken: kurz_csrftoken,
        },
        success: (data) => {
            showSuccess(data);
            $('#kurz_video').attr('src', '/kurz/video/' + data)[0].load();
        },
        error: () => {
            showError('Nay');
        }
    });
}