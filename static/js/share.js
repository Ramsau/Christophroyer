let share_clipboard;
let share_link;
async function share(event, service){
    event.stopPropagation();
    $(event.target).closest('.ui.dropdown').dropdown('hide');

    let url;
    if (service == 'copy') {
        await navigator.clipboard.writeText(share_link);

        showSuccess(share_clipboard);
        return;
    }
    else if (service == 'facebook') {
        url = 'https://www.facebook.com/sharer/sharer.php?u=' +
            encodeURIComponent(window.location.href) +
            '&amp;src=sdkpreparse'
    }
    else if (service == 'tumblr') {
        url = 'http://www.tumblr.com/share/link?url=' + encodeURIComponent(window.location.href);
    }
    else if (service == 'twitter') {
        url = 'https://twitter.com/intent/tweet?url=' + encodeURIComponent(window.location.href);
    }

}