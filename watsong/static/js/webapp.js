// @ts-check

/**
 * getCenter returns the center of an HTML element in x-y coordinates.
 *
 * @param {HTMLElement} elem element to find the center of
 * @return {{x: number, y: number}} center of elem in as object with .x and .y
 */
function getCenter(elem) {
    const { top, left, width } = elem.getBoundingClientRect();
    return { y: top + width / 2, x: left + width / 2 };
}

/**
 *  getCoord returns the position of a touch or click event
 *
 * @param {MouseEvent | TouchEvent} event touch/mouse event
 * @return {{x: number, y: number}} position of touch or click with .x and .y
 */
function getCoord(event) {
    if (event instanceof MouseEvent) {
        return { x: event.clientX, y: event.clientY };
    } else {
        // return coordinates of first touch
        const firstTouch = event.touches[0];
        return { x: firstTouch.clientX, y: firstTouch.clientY };
    }
}


/**
 * initializeDial makes the DOM element twistable and sends HTTP request when the twisting stops.
 *
 * @param {HTMLElement} elem is the `div` element that contains the image.
 * @param {string} dialName is the dial name to be sent to the backend
 */
function initializeDial(elem, dialName) {
    let currentAngle = 0, prevAngle = 0, initialAngle = 0, center = getCenter(elem);

    elem.onmousedown = onTwistStart;
    elem.ontouchstart = onTwistStart;

    /**
     * onTwistStart is called when a user touches or clicks down on `elem`
     *
     * @param {MouseEvent | TouchEvent} event touch/mouse event
     */
    function onTwistStart(event) {
        event.preventDefault();

        center = getCenter(elem);
        const { x, y } = getCoord(event);

        initialAngle = Math.atan2(x - center.x, y - center.y);

        document.onmouseup = onStopTwisting;
        document.onmousemove = onTwist;

        document.ontouchend = onStopTwisting;
        document.ontouchmove = onTwist;
    }

    /**
     * onTwist is called when a mouse moves while clicked, or dragged via touch.
     *
     * @param {MouseEvent | TouchEvent} event touch/mouse event
     */
    function onTwist(event) {
        event.preventDefault();

        const { x, y } = getCoord(event);

        const newAngle = Math.atan2(x - center.x, y - center.y);

        currentAngle = -(prevAngle + newAngle - initialAngle);

        $(elem).css("transform", `rotate(${currentAngle}rad)`);
    }


    /**
     * onStopTwisting is called when a user lets go of the dial (`elem`)
     */
    function onStopTwisting() {
        // stop twisting when mouse button is released
        document.onmouseup = null;
        document.onmousemove = null;

        document.ontouchend = null;
        document.ontouchmove = null;

        prevAngle = -currentAngle;

        const level = (currentAngle / (2 * Math.PI) + INITIAL_LEVEL + 5) % 1.0;

        GLOBAL.setFeel(dialName, level);

    }
}

/**
 * setSongs updates the DOM with new songs.
 *
 * @param {{title: string, artists: string[]}[]} songs
 */
function setSongs(songs) {
    const playlist = $('#playlist');

    playlist.empty();
    songs.forEach(song => {
        playlist.append(songRawHTML(song));
    });
}


function showPlaylist() {

    $.getJSON($SCRIPT_ROOT + '/jukebox/showPlaylist', {}, function ({ playlistId, success, msg }) {
        if (!success) {
            alert(msg);
            return;
        }

        const url = `https://open.spotify.com/embed/playlist/${playlistId}`;

        const playlist = $("#playlist");
        playlist.empty();
        playlist.append(`<iframe src="${url}" width="100%" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media" id="spotify"></iframe>`);

        const button = $("#subscribe-button");
        if (button.length === 0) {
            $("#jukebox-form").append(`<button type="button" id="subscribe-button" class="chunky-button" onclick="subscribeToPlaylist()">Subscribe</button>`);
        }

        GLOBAL.setPlaylistId(playlistId);
    });

}

function subscribeToPlaylist() {
    $.getJSON($SCRIPT_ROOT + '/jukebox/subscribe', { playlistId: GLOBAL.getPlaylistId() }, ({ msg }) => {
        alert(msg);
    });
}


/**
 * songRawHTML returns a raw HTML string representing the song element.
 *
 * @param {{title: string, artists: string[]}} song
 * @returns {string} raw HTML string for the song
 */
function songRawHTML(song) {
    return `<div class="song"><p class="title">${song.title}</p><p class="artist">${song.artists.join(", ")}</p></div>`;
}

// MAIN

/**
 *
 *
 * @return {{
 *  setFeel: (field: string, value: number, skipRequest?: boolean) => void, 
 *  getFeel: () => { [field: string] : number; }, 
 *  getPlaylistId: () => string, 
 *  setPlaylistId: (id: string) => void
 * }} 
 */
const StateModule = () => {
    /** @type {{ [field: string] : number; }} */
    let feel = {};
    let playlistId = null;

    /**
     * setFeel sets a field in `feel`
     *
     * @param {string} field
     * @param {number} value
     * @param {boolean} skipRequest whether to skip the HTTP request when updating the feel
     */
    const setFeel = (field, value, skipRequest = false) => {
        feel[field] = value;

        if (!skipRequest) {
            $.getJSON($SCRIPT_ROOT + '/jukebox/filter', feel, setSongs);
            const select = $("#" + field + "_value");
            select[0].innerText = Math.round(100 * value) + '%';
        }
    };

    /**
     * getFeel returns a copy of the feel object
     *
     * @return {{ [field: string] : number; }}
     */
    const getFeel = () => {
        /** @type {{ [field: string] : number; }} */
        const feelClone = {};
        for (const field in feel) {
            feelClone[field] = feel[field];
        }
        return feelClone;
    };


    /**
     * Gets the global playlist id
     *
     *  @return {string}
     */
    const getPlaylistId = () => playlistId;

    /**
     * Sets the global playlist id
     *
     * @param {string} newId new playlist id
     */
    const setPlaylistId = (newId) => {
        playlistId = newId;
    };

    return { setFeel, getFeel, getPlaylistId, setPlaylistId };
};

const GLOBAL = StateModule();
const INITIAL_LEVEL = 0.5;

$.each($('.dial'), function (_, elem) {
    const dial = $(elem).children('div')[0];
    initializeDial(dial, elem.id);
    GLOBAL.setFeel(elem.id, INITIAL_LEVEL, true);
});

