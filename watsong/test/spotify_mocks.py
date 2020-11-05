from unittest.mock import MagicMock


def between_worlds_mock() -> MagicMock:
    mock = MagicMock()
    mock.search.return_value = {
        "albums": {
            "href": "https://api.spotify.com/v1/search?query=a+girl+between+worlds&type=album&offset=0&limit=1",
            "items": [
                {
                    "album_type": "single",
                    "artists": [
                        {
                            "external_urls": {
                                "spotify": "https://open.spotify.com/artist/7ezrt08lody0nfis6owymp"
                            },
                            "href": "https://api.spotify.com/v1/artists/7ezrt08lody0nfis6owymp",
                            "id": "7ezrt08lody0nfis6owymp",
                            "name": "fatima yamaha",
                            "type": "artist",
                            "uri": "spotify:artist:7ezrt08lody0nfis6owymp",
                        }
                    ],
                    "external_urls": {
                        "spotify": "https://open.spotify.com/album/4MGNcuX4Vvhv2hhn1FwtDW"
                    },
                    "href": "https://api.spotify.com/v1/albums/4MGNcuX4Vvhv2hhn1FwtDW",
                    "id": "4MGNcuX4Vvhv2hhn1FwtDW",
                    "images": [
                        {
                            "height": 640,
                            "url": "https://i.scdn.co/image/ab67616d0000b273630f7ee95e279a92b285ed41",
                            "width": 640,
                        },
                        {
                            "height": 300,
                            "url": "https://i.scdn.co/image/ab67616d00001e02630f7ee95e279a92b285ed41",
                            "width": 300,
                        },
                        {
                            "height": 64,
                            "url": "https://i.scdn.co/image/ab67616d00004851630f7ee95e279a92b285ed41",
                            "width": 64,
                        },
                    ],
                    "name": "a girl between two worlds",
                    "release_date": "2015-02-13",
                    "release_date_precision": "day",
                    "total_tracks": 7,
                    "type": "album",
                    "uri": "spotify:album:4MGNcuX4Vvhv2hhn1FwtDW",
                }
            ],
            "limit": 1,
            "total": 1,
        }
    }
    mock.album_tracks.return_value = {
        "href": "https://api.spotify.com/v1/albums/4MGNcuX4Vvhv2hhn1FwtDW/tracks?offset=0&limit=50",
        "items": [
            {
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/7eZRt08LoDy0nfIS6OwyMP"
                        },
                        "href": "https://api.spotify.com/v1/artists/7eZRt08LoDy0nfIS6OwyMP",
                        "id": "7eZRt08LoDy0nfIS6OwyMP",
                        "name": "Fatima Yamaha",
                        "type": "artist",
                        "uri": "spotify:artist:7eZRt08LoDy0nfIS6OwyMP",
                    }
                ],
                "disc_number": 1,
                "duration_ms": 444337,
                "explicit": False,
                "external_urls": {
                    "spotify": "https://open.spotify.com/track/0Vpdt3FsW8m7nC4FDk3rfw"
                },
                "href": "https://api.spotify.com/v1/tracks/0Vpdt3FsW8m7nC4FDk3rfw",
                "id": "0Vpdt3FsW8m7nC4FDk3rfw",
                "is_local": False,
                "name": "Between Worlds",
                "preview_url": "https://p.scdn.co/mp3-preview/c324542386df66540bc4913a4df5e8cdd27cc577?cid=8170c7110cfb4503af349a6a8ea22fd3",
                "track_number": 1,
                "type": "track",
                "uri": "spotify:track:0Vpdt3FsW8m7nC4FDk3rfw",
            },
            {
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/7eZRt08LoDy0nfIS6OwyMP"
                        },
                        "href": "https://api.spotify.com/v1/artists/7eZRt08LoDy0nfIS6OwyMP",
                        "id": "7eZRt08LoDy0nfIS6OwyMP",
                        "name": "Fatima Yamaha",
                        "type": "artist",
                        "uri": "spotify:artist:7eZRt08LoDy0nfIS6OwyMP",
                    }
                ],
                "disc_number": 1,
                "duration_ms": 318951,
                "explicit": False,
                "external_urls": {
                    "spotify": "https://open.spotify.com/track/1QgNSDWdNMYBomYQbmekwU"
                },
                "href": "https://api.spotify.com/v1/tracks/1QgNSDWdNMYBomYQbmekwU",
                "id": "1QgNSDWdNMYBomYQbmekwU",
                "is_local": False,
                "name": "Half Moon Rising",
                "preview_url": "https://p.scdn.co/mp3-preview/6c7bc5e13a71e5e014cdade333562db72022a925?cid=8170c7110cfb4503af349a6a8ea22fd3",
                "track_number": 2,
                "type": "track",
                "uri": "spotify:track:1QgNSDWdNMYBomYQbmekwU",
            },
            {
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/7eZRt08LoDy0nfIS6OwyMP"
                        },
                        "href": "https://api.spotify.com/v1/artists/7eZRt08LoDy0nfIS6OwyMP",
                        "id": "7eZRt08LoDy0nfIS6OwyMP",
                        "name": "Fatima Yamaha",
                        "type": "artist",
                        "uri": "spotify:artist:7eZRt08LoDy0nfIS6OwyMP",
                    }
                ],
                "disc_number": 1,
                "duration_ms": 283738,
                "explicit": False,
                "external_urls": {
                    "spotify": "https://open.spotify.com/track/0pzUyMlx7b7xJkuKng5d8H"
                },
                "href": "https://api.spotify.com/v1/tracks/0pzUyMlx7b7xJkuKng5d8H",
                "id": "0pzUyMlx7b7xJkuKng5d8H",
                "is_local": False,
                "name": "Plum Jelly",
                "preview_url": "https://p.scdn.co/mp3-preview/e1ce9af6f686a4ca010a6fa1e47b2dcd26a663c1?cid=8170c7110cfb4503af349a6a8ea22fd3",
                "track_number": 3,
                "type": "track",
                "uri": "spotify:track:0pzUyMlx7b7xJkuKng5d8H",
            },
            {
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/7eZRt08LoDy0nfIS6OwyMP"
                        },
                        "href": "https://api.spotify.com/v1/artists/7eZRt08LoDy0nfIS6OwyMP",
                        "id": "7eZRt08LoDy0nfIS6OwyMP",
                        "name": "Fatima Yamaha",
                        "type": "artist",
                        "uri": "spotify:artist:7eZRt08LoDy0nfIS6OwyMP",
                    }
                ],
                "disc_number": 1,
                "duration_ms": 446510,
                "explicit": False,
                "external_urls": {
                    "spotify": "https://open.spotify.com/track/5N720bYInxSsiUDvBOLM3C"
                },
                "href": "https://api.spotify.com/v1/tracks/5N720bYInxSsiUDvBOLM3C",
                "id": "5N720bYInxSsiUDvBOLM3C",
                "is_local": False,
                "name": "What's a Girl to Do",
                "preview_url": "https://p.scdn.co/mp3-preview/d91cde080cf964db0a623365033f3c98909458e4?cid=8170c7110cfb4503af349a6a8ea22fd3",
                "track_number": 4,
                "type": "track",
                "uri": "spotify:track:5N720bYInxSsiUDvBOLM3C",
            },
            {
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/7eZRt08LoDy0nfIS6OwyMP"
                        },
                        "href": "https://api.spotify.com/v1/artists/7eZRt08LoDy0nfIS6OwyMP",
                        "id": "7eZRt08LoDy0nfIS6OwyMP",
                        "name": "Fatima Yamaha",
                        "type": "artist",
                        "uri": "spotify:artist:7eZRt08LoDy0nfIS6OwyMP",
                    }
                ],
                "disc_number": 1,
                "duration_ms": 376280,
                "explicit": False,
                "external_urls": {
                    "spotify": "https://open.spotify.com/track/1wWGLxqWFapa9L05T9e9YQ"
                },
                "href": "https://api.spotify.com/v1/tracks/1wWGLxqWFapa9L05T9e9YQ",
                "id": "1wWGLxqWFapa9L05T9e9YQ",
                "is_local": False,
                "name": "At the Foot of Mt. Arrarat",
                "preview_url": "https://p.scdn.co/mp3-preview/28e2c772f56c7a63b8bc974242c6e03868640dad?cid=8170c7110cfb4503af349a6a8ea22fd3",
                "track_number": 5,
                "type": "track",
                "uri": "spotify:track:1wWGLxqWFapa9L05T9e9YQ",
            },
            {
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/7eZRt08LoDy0nfIS6OwyMP"
                        },
                        "href": "https://api.spotify.com/v1/artists/7eZRt08LoDy0nfIS6OwyMP",
                        "id": "7eZRt08LoDy0nfIS6OwyMP",
                        "name": "Fatima Yamaha",
                        "type": "artist",
                        "uri": "spotify:artist:7eZRt08LoDy0nfIS6OwyMP",
                    }
                ],
                "disc_number": 1,
                "duration_ms": 226998,
                "explicit": False,
                "external_urls": {
                    "spotify": "https://open.spotify.com/track/4viXkNYb7kyvdd25ppIqmk"
                },
                "href": "https://api.spotify.com/v1/tracks/4viXkNYb7kyvdd25ppIqmk",
                "id": "4viXkNYb7kyvdd25ppIqmk",
                "is_local": False,
                "name": "Sushi and Baklava",
                "preview_url": "https://p.scdn.co/mp3-preview/5e3c4f456c5fad27472748e4643bfa61c9487880?cid=8170c7110cfb4503af349a6a8ea22fd3",
                "track_number": 6,
                "type": "track",
                "uri": "spotify:track:4viXkNYb7kyvdd25ppIqmk",
            },
            {
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/7eZRt08LoDy0nfIS6OwyMP"
                        },
                        "href": "https://api.spotify.com/v1/artists/7eZRt08LoDy0nfIS6OwyMP",
                        "id": "7eZRt08LoDy0nfIS6OwyMP",
                        "name": "Fatima Yamaha",
                        "type": "artist",
                        "uri": "spotify:artist:7eZRt08LoDy0nfIS6OwyMP",
                    }
                ],
                "disc_number": 1,
                "duration_ms": 209435,
                "explicit": False,
                "external_urls": {
                    "spotify": "https://open.spotify.com/track/6ezatiaJEBHpi72EjnTl9s"
                },
                "href": "https://api.spotify.com/v1/tracks/6ezatiaJEBHpi72EjnTl9s",
                "id": "6ezatiaJEBHpi72EjnTl9s",
                "is_local": False,
                "name": "To Do Two",
                "preview_url": "https://p.scdn.co/mp3-preview/e5bf9594b35a7f20bc846c389eb7602eedfa2095?cid=8170c7110cfb4503af349a6a8ea22fd3",
                "track_number": 7,
                "type": "track",
                "uri": "spotify:track:6ezatiaJEBHpi72EjnTl9s",
            },
        ],
        "limit": 50,
        "next": None,
        "offset": 0,
        "previous": None,
        "total": 7,
    }
    mock.audio_features.return_value = [
        {
            "danceability": 0.75,
            "energy": 0.611,
            "key": 10,
            "loudness": -8.053,
            "mode": 0,
            "speechiness": 0.0538,
            "acousticness": 0.0832,
            "instrumentalness": 0.837,
            "liveness": 0.0708,
            "valence": 0.546,
            "tempo": 131.045,
            "type": "audio_features",
            "id": "0Vpdt3FsW8m7nC4FDk3rfw",
            "uri": "spotify:track:0Vpdt3FsW8m7nC4FDk3rfw",
            "track_href": "https://api.spotify.com/v1/tracks/0Vpdt3FsW8m7nC4FDk3rfw",
            "analysis_url": "https://api.spotify.com/v1/audio-analysis/0Vpdt3FsW8m7nC4FDk3rfw",
            "duration_ms": 444338,
            "time_signature": 4,
        }
    ]
    return mock
