function less(button) {
    const img = $(button).parent().children("img")[0];
    img.degrees = img.degrees === undefined ? 0 : img.degrees;
    img.degrees = img.degrees + 36;
    $(img).rotate(img.degrees);
}

function more(button) {
    console.log($(button));
    const img = $(button).parent().children("img")[0];
    img.degrees = img.degrees === undefined ? 0 : img.degrees;
    img.degrees = img.degrees - 36;
    $(img).rotate(img.degrees);
}

const beachSongs = [{
    "song": "Under the Boardwalk",
    "album": "Under the Boardwalk",
    "artist": "The Drifters"
}, {
    "song": "What's Love Got to Do with It",
    "album": "Private Dancer",
    "artist": "Tina Turner"
}, {
    "song": "This Is The Life",
    "album": "This Is The Life",
    "artist": "Amy Macdonald"
}, {
    "song": "I'll Wait",
    "album": "Golden Hour",
    "artist": "Sasha Sloan, Kygo"
}]

function onInput() {
    // input is always "songs for the beach"
    addSongs(beachSongs);
}

beachEnergySongs = [
    {
        "song": "Malibu",
        "album": "Under the Boardwalk",
        "artist": "Miley Cyrus"
    },
    {
        "song": "Margaritaville",
        "album": "Under the Boardwalk",
        "artist": "Jimmy Buffet"
    },
    {
        "song": "Under the Boardwalk",
        "album": "Under the Boardwalk",
        "artist": "The Drifters"
    }, {
        "song": "What's Love Got to Do with It",
        "album": "Private Dancer",
        "artist": "Tina Turner"
    }, {
        "song": "This Is The Life",
        "album": "This Is The Life",
        "artist": "Amy Macdonald"
    }, {
        "song": "I'll Wait",
        "album": "Golden Hour",
        "artist": "Sasha Sloan, Kygo"
    }
]

function addEnergy(button) {
    more(button);
    addSongs(beachEnergySongs);
}

beachEnergyLyricsSongs = [
    {
        "song": "Californication",
        "album": "Under the Boardwalk",
        "artist": "Red Hot Chili Peppers"
    },
    {
        "song": "Harder Better Faster Stronger",
        "album": "Under the Boardwalk",
        "artist": "Daft Punk"
    },
    {
        "song": "Margaritaville",
        "album": "Under the Boardwalk",
        "artist": "Jimmy Buffet"
    },
    {
        "song": "Under the Boardwalk",
        "album": "Under the Boardwalk",
        "artist": "The Drifters"
    },
    {
        "song": "This Is The Life",
        "album": "This Is The Life",
        "artist": "Amy Macdonald"
    },
    {
        "song": "I'll Wait",
        "album": "Golden Hour",
        "artist": "Sasha Sloan, Kygo"
    }
]

function removeLyrics(button) {
    less(button)
    addSongs(beachEnergyLyricsSongs)
}

