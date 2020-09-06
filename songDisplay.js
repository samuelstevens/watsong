function reload() {
    alert("Getting new songs!");
}

function addSongs(songs) {
    // add songs as children to #playlist
    setTimeout(() => {
        // 1. clear all songs
        $("#playlist").empty();
        // 2. for (song in songs)
        songs.forEach(song => {
            // 3.   add song to #playlist
            $("#playlist").append(`<div class="song"><p class="title">${song.song}</p><p class="artist">${song.artist}</p></div>`)
        })
    }, 0);
}

function songDisplay() {
    // set up initial transform
    $.each($(".dial > img"), (index, img) => {
        img.degrees = 0;
    })

    addSongs([]);
}

function showPlaylist() {
    setTimeout(() => {
        const playlist = $("#playlist");
        playlist.empty();
        playlist.append('<iframe src="https://open.spotify.com/embed/playlist/6pK46CrbkO1az5HaUmqpow"width="100%" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media" id="spotify"></iframe>')
    }, 0);
}

songDisplay();
