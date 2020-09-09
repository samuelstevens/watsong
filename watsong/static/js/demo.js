// @ts-nocheck

function less(button) {
  const img = $(button).parent().children("img")[0];
  img.degrees = img.degrees - 45;
  $(img).css("rotate", `${img.degrees}deg`);
}

function more(button) {
  const img = $(button).parent().children("img")[0];
  img.degrees = img.degrees + 45;
  $(img).css("rotate", `${img.degrees}deg`);
}

function setSongs(songs) {
  // set songs as children to #playlist
  setTimeout(() => {
    // 1. clear all songs
    $("#playlist").empty();
    // 2. for (song in songs)
    songs.forEach((song) => {
      // 3.   add song to #playlist
      $("#playlist").append(
        `<div class="song"><p class="title">${song.song}</p><p class="artist">${song.artist}</p></div>`
      );
    });
  }, 500);
}

function main() {
  // set up initial transform
  $.each($(".dial > img"), (index, img) => {
    img.degrees = -31;
  });

  setSongs([]);
}

const beachSongs = [
  {
    song: "Under the Boardwalk",
    album: "Under the Boardwalk",
    artist: "The Drifters",
  },
  {
    song: "What's Love Got to Do with It",
    album: "Private Dancer",
    artist: "Tina Turner",
  },
  {
    song: "This Is The Life",
    album: "This Is The Life",
    artist: "Amy Macdonald",
  },
  {
    song: "I'll Wait",
    album: "Golden Hour",
    artist: "Sasha Sloan, Kygo",
  },
];

$("#query-form").submit(function (e) {
  e.preventDefault(); // avoid to execute the actual submit of the form.

  var form = $(this);

  $.getJSON($SCRIPT_ROOT + "_nat_lang_query", form.serialize())
    .done(result => {
      if (result.error) {
        alert(result.error);
      } else {
        setSongs(result);
      }

    })
    .fail(error => {
      alert(error);
    });
});

const beachEnergySongs = [
  {
    song: "Malibu",
    album: "Under the Boardwalk",
    artist: "Miley Cyrus",
  },
  {
    song: "Margaritaville",
    album: "Under the Boardwalk",
    artist: "Jimmy Buffet",
  },
  {
    song: "Under the Boardwalk",
    album: "Under the Boardwalk",
    artist: "The Drifters",
  },
  {
    song: "What's Love Got to Do with It",
    album: "Private Dancer",
    artist: "Tina Turner",
  },
  {
    song: "This Is The Life",
    album: "This Is The Life",
    artist: "Amy Macdonald",
  },
  {
    song: "I'll Wait",
    album: "Golden Hour",
    artist: "Sasha Sloan, Kygo",
  },
];

function addEnergy(button) {
  more(button);
  setSongs(beachEnergySongs);
}

const beachEnergyLyricsSongs = [
  {
    song: "Californication",
    album: "Under the Boardwalk",
    artist: "Red Hot Chili Peppers",
  },
  {
    song: "Harder Better Faster Stronger",
    album: "Under the Boardwalk",
    artist: "Daft Punk",
  },
  {
    song: "Margaritaville",
    album: "Under the Boardwalk",
    artist: "Jimmy Buffet",
  },
  {
    song: "Under the Boardwalk",
    album: "Under the Boardwalk",
    artist: "The Drifters",
  },
  {
    song: "This Is The Life",
    album: "This Is The Life",
    artist: "Amy Macdonald",
  },
  {
    song: "I'll Wait",
    album: "Golden Hour",
    artist: "Sasha Sloan, Kygo",
  },
];

function removeLyrics(button) {
  less(button);
  setSongs(beachEnergyLyricsSongs);
}

function showPlaylist() {
  setTimeout(() => {
    $("#playlist").empty();
    $("#playlist").append(
      '<iframe src="https://open.spotify.com/embed/playlist/6pK46CrbkO1az5HaUmqpow" width="100%" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media" id="spotify"></iframe>'
    );
  }, 500);
}

main();
