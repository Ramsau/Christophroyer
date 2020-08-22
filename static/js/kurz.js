function updateCharCount() {
    $('#chars_remaining').html(255 - $('#kurz_text').val().length);
}

let kurz_submitUrl;
let kurz_csrftoken;
let kurz_processingText;
function submitText(text) {
    showInfo(kurz_processingText);
    $.ajax({
        url: kurz_submitUrl,
        method: 'POST',
        data: {
            text: text,
            csrfmiddlewaretoken: kurz_csrftoken,
        },
        success: (data) => {
            showSuccess(kurz_success);
            $('#kurz_video').attr('src', '/kurz/video/' + data)[0].load();

            window.history.replaceState(null, null, '?vid=' + data)
            $('#share_facebook').attr('href',
                'https://www.facebook.com/sharer/sharer.php?u=' +
                encodeURIComponent(window.location.href) +
                '&amp;src=sdkpreparse'
            )

            $('#share_tumblr').attr('href',
                'http://www.tumblr.com/share/link?url=' +
                encodeURIComponent(window.location.href)
            )

            $('#share_twitter').attr('href',
                'https://twitter.com/intent/tweet?text=kurzspricht.at&url=' +
                encodeURIComponent(window.location.href)
            )
        },
        error: () => {
            showError(kurz_error);
        }
    });
}
