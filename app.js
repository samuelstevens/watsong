/**
 * This is an example of a basic node.js script that performs
 * the Authorization Code oAuth2 flow to authenticate against
 * the Spotify Accounts.
 *
 * For more information, read
 * https://developer.spotify.com/web-api/authorization-guide/#authorization_code_flow
 */
const express = require('express'); // Express web server framework
const request = require('request'); // "Request" library
const cors = require('cors');
const querystring = require('querystring');
const cookieParser = require('cookie-parser');

// Spotify credentials
// email: 7alex7li@gmail.com
// username: watsong1
// password: watsong1
const client_id = 'cabbb7f1ed864a9d8cd4db6ec60ae7da';
const client_secret = '87edc5fa9ab6409784f1c11237e77515';
const redirect_uri = 'http://localhost:8888/callback';

/**
 * Generates a random string containing numbers and letters
 * @param  {number} length The length of the string
 * @return {string} The generated string
 */
const generateRandomString = function (length) {
    let text = '';
    let possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

    for (let i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
};

const stateKey = 'spotify_auth_state';

const app = express();

app.use(express.static(__dirname + '/public'))
    .use(cors())
    .use(cookieParser());

app.get('/login', function (req, res) {
    const state = generateRandomString(16);
    res.cookie(stateKey, state);

    // your application requests authorization
    const scope = 'playlist-modify-private playlist-modify-public playlist-modify';
    res.redirect('https://accounts.spotify.com/authorize?' +
        querystring.stringify({
            response_type: 'code',
            client_id: client_id,
            scope: scope,
            redirect_uri: redirect_uri,
            state: state
        }));
});

app.get('/callback', function (req, res) {
    // your application requests refresh and access tokens
    // after checking the state parameter

    var code = req.query.code || null;
    var state = req.query.state || null;
    var storedState = req.cookies ? req.cookies[stateKey] : null;

    if (state === null || state !== storedState) {
        res.redirect('/#' +
            querystring.stringify({
                error: 'state_mismatch'
            }));
    } else {
        res.clearCookie(stateKey);
        var authOptions = {
            url: 'https://accounts.spotify.com/api/token',
            form: {
                code: code,
                redirect_uri: redirect_uri,
                grant_type: 'authorization_code'
            },
            headers: {
                'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
            },
            json: true
        };

        request.post(authOptions, function (error, response, body) {
            if (!error && response.statusCode === 200) {

                var access_token = body.access_token,
                    refresh_token = body.refresh_token;

                var options = {
                    url: 'https://api.spotify.com/v1/me',
                    headers: {'Authorization': 'Bearer ' + access_token},
                    json: true
                };

                // use the access token to access the Spotify Web API
                request.get(options, function (error, response, body) {
                    console.log(body);
                });

                // we can also pass the token to the browser to make requests from there
                res.redirect('/#' +
                    querystring.stringify({
                        access_token: access_token,
                        refresh_token: refresh_token
                    }));
            } else {
                res.redirect('/#' +
                    querystring.stringify({
                        error: 'invalid_token'
                    }));
            }
        });
    }
});
app.get('/refresh_token', function (req, res) {
    // requesting access token from refresh token
    const refresh_token = req.query.refresh_token;
    const authOptions = {
        url: 'https://accounts.spotify.com/api/token',
        headers: {'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))},
        form: {
            grant_type: 'refresh_token',
            refresh_token: refresh_token
        },
        json: true
    };

    request.post(authOptions, function (error, response, body) {
        if (!error && response.statusCode === 200) {
            const access_token = body.access_token;
            res.send({
                'access_token': access_token
            });
        }
    });
});

app.get('/make_playlist', function (req, res) {
    const id = req.query.user_id;
    const access_token = req.query.access_token;
    const create_options = {
        url: `https://api.spotify.com/v1/users/${id}/playlists`,
        headers: {
            'Authorization': "Bearer " + access_token,
            'Content-Type': 'application/json',
        },
        body: {
            name: "Test playlist",
        },
        json: true
    }
    request.post(create_options, function (error, response) {
        if(error){
            console.error("In app.js make_playlist:");
            console.error(error);
        }
        const playlistId = response.body.id;
        const song_options = {
            url: `https://api.spotify.com/v1/playlists/${playlistId}/tracks`,
            headers: {
                'Authorization': "Bearer " + access_token,
                'Content-Type': 'application/json',
            },
            body: {
                uris: ['spotify:track:48UPSzbZjgc449aqz8bxox',
                    'spotify:track:5W3cjX2J3tjhG8zb6u0qHn',
                    'spotify:track:4EEjMyQub6tgFVshlM9j1M',
                    'spotify:track:65jrjEhWfAvysKfnojk1i0',
                    'spotify:track:1sihSJEXrJJgyaLd4DeZYq',
                    'spotify:track:6Q3K9gVUZRMZqZKrXovbM2',
                ]
            },
            json: true
        }
        request.post(song_options, function (error) {
            if(error){
                console.error("In app.js make_playlist:");
                console.error(error);
            }
            res.send(playlistId);
        });
    });
});


console.log('Listening on 8888');
app.listen(8888);