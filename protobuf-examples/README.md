# Protobuf notes

Scraping the album page produces a lot of minifed JS and very little HTML. However, the page does include a data structure that looks like a [protobuf](https://developers.google.com/protocol-buffers).

This directory contains some example protobuf output that I used while reverse engineering enough to scrape the album. Notes about what I found are in this file.

## Notes

* Can't correlate info from the [API](https://developers.google.com/photos/library/guides/list#listing-album-contents) with info parsed from saved page since no IDs overlap
* In the HTML returned, the parameter to `AF_initDataCallback(...)` seems to be a protobuf
* You can write out the protobuf info as a JSON file using `--save-protobuf PATH/TO/FILENAME` and load it again with `--load FILENAME`
    * This is useful in debugging, where you can save the structure of several versions of an album to compare
    * It is also useful if you're changing the output HTML, since you can regenerate it without using the internet

## Structure

Overall structure:

```
[
    null,
    [list of images],
    "",
    [album info including sharing],
    [list of enrichments]
]
```

### Images

Format for the list of images. Ordered the same as display in the album.

```
[
    "AF1QipOlQgoYJGjKaFOMHJkYqQVH4zxkn9brxgwXHhq2", # Not the ID. part of productURL? seems mostly stable
    [
        "baseURL",
        <width>,
        <height>,
        null,
        [],
        null,
        [],
        null,
        null,
        [
            13155507
        ]
    ],
    <unix epoch, date the photo was taken>,
    "TOt7ob2rr6UBovGSirT8orZJDaM", # not the ID, but stable across requests & remove/re-add to album
    <tz offset, seconds, probably for date taken>,
    <unix epoch, date the photo was added to album?>,
    [
        "<owner identifier>" # data-actor-media-key - google account that the image is from?
    ],
    [ # same in all images
        [
            2
        ],
        [
            31,
            false,
            true
        ],
        [
            36,
            false,
            true
        ],
        [
            8
        ],
        [
            21
        ],
        [
            19
        ],
        [
            22
        ]
    ],
    2,
    null,
    null,
    null,
    [],
    null,
    19222,
    [],
    {
        "101428965": [
            0,
            "vdh9cohf070000000000004k" # ordering string
        ]
    }
],
```

### Album

Includes album info and sharing info

```
    [
        "AF1QipOsyTRCCkFhI8kRqZiQ8K5ICY_836mUn6wQNmiPRZUAxaGLGL4pMqylMVe04RNbDA", # sharing identifier?
        "<album name>",
        [ # Cover info
            1654022822000,
            1654033897000,
            null,
            null,
            1654554485407,
            [
                1654022822000,
                <tz offset, in seconds>
            ],
            [
                1654033897000,
                <tz offset, in seconds>
            ],
            1654714018456,
            1654554485407
        ],
        "<download URL, changes every save>",
        [ # cover image?
            "https://lh3.googleusercontent.com/di2eIfHVeI03KAvSkwflqo1SjAEKf2-hMh-Sq6xnbONyKReACEd2FHywgeVidqCbaBoEM26tUtJEBZGQedTToHHBHodBk3beWdz-HGGY4C2s9mekJ2ZAj2_2bNXa3MunO98pVAtIIwE",
            4608,
            3456,
            null,
            [],
            null,
            [],
            null,
            [
                4608,
                3456,
                1,
                null,
                [
                    "OnePlus",
                    "ONEPLUS A6013",
                    null,
                    4.25,
                    1.7,
                    800,
                    0.05,
                    null,
                    1
                ]
            ],
            [
                10511410
            ]
        ],
        [ # Owner info
            "<owner identifier>", # owner ID
            "108435023741049154519",
            null,
            "<owner avatar image>",
            null,
            [
                "<owner identifier>",
                "108435023741049154519"
            ],
            null,
            null,
            null,
            null,
            null,
            [
                "<owner full name>",
                1,
                null,
                "<owner first name?>"
            ],
            [
                "<owner avatar again?>"
            ],
            null,
            null,
            null,
            [],
            [
                2
            ]
        ],
        [
            [
                31,
                false,
                true
            ],
            [
                36,
                false,
                true
            ],
            [
                8
            ],
            [
                21
            ],
            [
                24,
                false,
                true
            ],
            [
                25,
                false,
                true
            ],
            [
                32,
                false,
                true
            ]
        ],
        "AF1QipOsyTRCCkFhI8kRqZiQ8K5ICY_836mUn6wQNmiPRZUAxaGLGL4pMqylMVe04RNbDA",
        true,
        [
            [
                "<owner identifier>",
                "108435023741049154519",
                null,
                "<owner avatar image>",
                null,
                [
                    "<owner identifier>",
                    "108435023741049154519"
                ],
                null,
                null,
                null,
                null,
                null,
                [
                    "<owner full name>",
                    1,
                    null,
                    "<owner first name?>"
                ],
                [
                    "<owner avatar again?>"
                ],
                null,
                null,
                null,
                [],
                [
                    2
                ]
            ]
        ],
        [
            true,
            true,
            [
                [
                    1,
                    1
                ],
                [
                    2,
                    1
                ],
                [
                    1,
                    2
                ],
                [
                    2,
                    2
                ],
                [
                    3,
                    1
                ]
            ],
            [
                3
            ]
        ],
        null,
        null,
        null,
        null,
        [],
        null,
        null,
        "",
        "MktDaHBHQlNHSzFFdFo4WEVGZjRfbE9HUEFpRDNn",
        1,
        2,
        null,
        [],
        null,
        [
            19998
        ],
        0,
        null,
        [
            [
                [
                    "<owner identifier>",
                    "108435023741049154519"
                ],
                "<owner avatar image>",
                null,
                [
                    "<owner full name>",
                    1,
                    null,
                    "<owner first name?>"
                ],
                [
                    1654714010900,
                    1654554485407,
                    []
                ],
                1,
                "",
                "",
                [],
                [],
                null,
                [
                    "<owner avatar again?>"
                ],
                null,
                2
            ]
        ],
        null,
        [
            1,
            false
        ],
        1,
        "<sharing URL>",
        null,
        5,
        [],
        0,
        {
            "117194011": [
                [
                    null,
                    null,
                    []
                ]
            ]
        }
    ],
```

### Enhancements

Text, maps and locations are all 'enhancements' and in the same array. Order seems to be the order they were added to the album.

All enhancements have a dictionary as the 17th element, with 2 keys:

* `99218341` = stable key for enrichment info
    * 1=text, 2=location, 3=map
* `101428965` for location info (see below)

### Text

```
[
    "AF1QipPIawvW8shUbT4NGrGEPaZdIEgTBE900SoMc-oudntXjsUWy5x4",
    null,
    null,
    null,
    null,
    null,
    null,
    [],
    null,
    null,
    null,
    null,
    [],
    null,
    null,
    [],
    {
        "99218341": [
            [
                1,  # always 1
                [
                    "text to display"
                ]
            ]
        ],
        "101428965": [
            0,
            "vdh9cohf0700g0000000004a" # ordering string
        ]
    }
]
```

### Location

```
[
    "AF1QipNv0h78Co3shx2KGoE-UeBbJWdRtWUbKuLmRMovvO1hZCErC0UQ",
    null,
    null,
    null,
    null,
    null,
    null,
    [],
    null,
    null,
    null,
    null,
    [],
    null,
    null,
    [],
    {
        "99218341": [
            [
                2, # always 2
                null,
                [
                    null,
                    [
                        [
                            3, # 3 indicates a location?
                            [
                                [
                                    "6090683026124656563", # different between entries, consistent for location, possibly map tile?
                                    "13515749891091067787" # ditto
                                ]
                            ],
                            null,
                            "Big text (main location)",
                            "small text (subscript, eg province, country)", # this and later not always present
                            [
                                <lat>,
                                <lon>
                            ],
                            null,
                            0
                        ]
                    ]
                ]
            ]
        ],
        "101428965": [
            0,
            "vdh9cohf06vv00000000004a" # ordering string
        ]
    }
],
```

### Map

```
[
    "AF1QipOqAHcPqviaaFzB5JJeU4dKI6jMM_wOunhh3xW8Pt3lFCN9C9uu",
    null,
    null,
    null,
    null,
    null,
    null,
    [],
    null,
    null,
    null,
    null,
    [],
    null,
    null,
    [],
    {
        "99218341": [
            [
                3,
                null,
                null,
                [
                    null,
                    null,
                    null,
                    [
                        [ # source location - same inner array as a Location
                            3,
                            [
                                [
                                    "6090683026124656563",
                                    "13515749891091067787"
                                ]
                            ],
                            null,
                            "big text (main location)",
                            "small text (context info)",
                            [
                                <lat>,
                                <lon>
                            ],
                            null,
                            0
                        ]
                    ],
                    [
                        [ # destination location - same inner array as a Location
                            3,
                            [
                                [
                                    "5177074476702594547",
                                    "1472861389740886636"
                                ]
                            ],
                            null,
                            "big text (main location)",
                            "small text (context info)",
                            [
                                <lat>,
                                <lon>
                            ],
                            null,
                            0
                        ]
                    ]
                ]
            ]
        ],
        "101428965": [
            0,
            "vdh9cohf06vto0000000004a" # ordering string
        ]
    }
],
```


## Images

* Ref:https://developers.google.com/photos/library/guides/access-media-items#base-urls
* `baseUrl` can be used to download the file, or download it with a max height and/or max width
* If you request the baseUrl too many times, Google blocks you, not sure how long
* downloaded images include most EXIF data but not location info (intentionally)
* `productUrl` directs to the image inside google photos, but I don't think this can be accessed programatically
    * the full image with all metadata can be downloade from here

## Ordering

* All elements have a dictionary with key `101428965` that always has `[0, <ordering string>]`
* ordering string:
    * usually shares a prefix
        * in the test album `vdh9` appears repeatedly - possibly album prefix or encoding info that's the same for a given album
    * ends in `k` = image
    * ends in `a` = enrichment
    * often ends with `000000000004k` or `00000000004a`, possibly because very small album
        * large album has more variety in those characters
    * sometimes ending omitted eg `vdh9d3bi` vs `vdh9cohf070000000000004k` in the same album
        * or `vdcpo87k` vs `vdcpo87k06vt00000000004a`
* changing ordering changes 1 character in the string
    * item that was click-and-dragged is the one that changes
    * string seems to sort a > b, 1 > 2
    * aka naive sorting based on the strings works, including the short strings

### Details - album with 2 images

Order: 1, 2
```
vdh9cohf06vr00000000004k
vdh9cohf06vu00000000004k
           ^
```

Order: 2, 1
```
vdh9cohf06vq00000000004k
vdh9cohf06vr00000000004k
           ^
```

difference:
```
r0,u0
q0,r0
```

### Details - album with 2 text boxes

* 1 = text box with 'text 1'
* 2 = text box with 'text 2'

Order: 1,2
```
1: vdh9cohf06vq40000000004a
2: vdh9cohf06vq80000000004a
               ^
```
difference: `q4,q8`

Order: 2,1
```
1: vdh9cohf06vq40000000004a
2: vdh9cohf06vp40000000004a
              ^
```
difference: `q4,p4`

Order: 1,2 again
```
1: vdh9cohf06vo40000000004a
2: vdh9cohf06vp40000000004a
              ^
```
difference: `o4,p4`

Does it depend on which one I clicked on?

Order: 2,1 again - dragged 'text 2'
```
1: vdh9cohf06vo40000000004a
2: vdh9cohf06vn40000000004a
              ^
```
difference: `o4,n4`

text 2 changed, probably because it's the one I touched

Order: 1,2 again2 dragged 'text 1' up
```
1: vdh9cohf06vm40000000004a
2: vdh9cohf06vn40000000004a
              ^
```
difference: `m4,n4`

* alphabet sort puts them in the correct order
* probably an encoded something where a bit moves/changes and it affects the ASCII version

## Links

### photos api

* https://pypi.org/project/gphotos-sync/ ref for how used
* https://github.com/gilesknap/gphotos-sync/tree/master/gphotos
* https://gilesknap.github.io/gphotos-sync/main/tutorials/oauth2.html
* https://developers.google.com/photos/library/guides/get-started
* https://developers.google.com/photos/library/guides/list#listing-album-contents
* https://developers.google.com/photos/library/reference/rest/v1/albums
* https://github.com/alexcrist/scrape-google-photos

### auth

* https://developers.google.com/photos/library/guides/authentication-authorization
* https://google-auth.readthedocs.io/en/latest/user-guide.html
* https://oauthlib.readthedocs.io/en/latest/oauth2/clients/client.html
* https://github.com/requests/requests-oauthlib
* https://requests-oauthlib.readthedocs.io/en/latest/examples/google.html
