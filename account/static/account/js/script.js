$('#following_btn').click(function(){

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
const request = new Request(
    /* URL */,
    {headers: {'X-CSRFToken': csrftoken}}
);
fetch(request, {
    method: 'POST',
    mode: 'same-origin'  // Do not send CSRF token to another domain.
}).then(function(response) {
});

var user_id = $('#following_btn').attr('data-id')
var follow = $('#following_btn').text()

if (follow == 'Follow'){
    let url = '/account/follow/'
    let btn_text = 'unfollow'
    let btn_class = 'btn btn-warning text-center mx-auto'
}
else if (follow == 'Unfollow') {
    let url = '/account/unfollow/'
    let btn_text = 'follow'
    let btn_class = 'btn btn-primary text-center mx-auto'
}

$.ajax({
    url : url,
    method : 'POST',
    data: {
    'user_id' : user_id,
    },
    success: function(data){
        if (data['status'] == 'ok') {
        $('#following_btn').text(btn_text)
        $('#following_btn').attr({'class':btn_class})
        }
    }
});

});




