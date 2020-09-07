/**
 * Obtains parameters from the hash of the URL
 * @return Object
 */
function getHashParams() {
    const hashParams = {};
    let e, r = /([^&;=]+)=?([^&;]*)/g,
        q = window.location.hash.substring(1);
    while (e = r.exec(q)) {
        hashParams[e[1]] = decodeURIComponent(e[2]);
    }
    return hashParams;
}

const params = getHashParams();

let access_token = params.access_token,
    refresh_token = params.refresh_token,
    error = params.error;

let user_id;

if (error) {
    alert('There was an error during the authentication');
} else {
    if (access_token) {
        $.ajax({
            url: 'https://api.spotify.com/v1/me',
            headers: {
                'Authorization': 'Bearer ' + access_token
            },
            success: function (response) {
                user_id = response.id
                $('#login').hide();
            }
        });
    } else {
        // render initial screen
        $('#login').show();
    }

    function refreshToken() {
        $.ajax({
            url: '/refresh_token',
            data: {
                'refresh_token': refresh_token
            }
        }).done(function (data) {
            access_token = data.access_token;
        });
    }
}

function createPlaylist(then) {
    $.ajax({
        url: '/make_playlist',
        data: {
            'user_id': user_id,
            'access_token': access_token,
        },
    }).done(function (playlist_id) {
        then(playlist_id);
    });
}


function getPlaylist(songs) {
    $.post()
}
