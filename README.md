# Readme

## Problem

Export of Google Photos albums sucks. Google Takeout only does photos. The [API](https://developers.google.com/photos/library/reference/rest/v1/albums/) only returns name and cover information, and no part of the API returns "enrichments" like text and locations, with [no plans to add that](https://issuetracker.google.com/issues/129050144). The page returned from a HTTP request or to the browser is unreadable JS garbage, with all the functions minified and the content in obtuse data strings.

## Goal

Write a script that can export a Google Photos album into human-readable HTML, CSS and Javascript that I can host anywhere.

I couldn't find any projects that did this already (but please let me know if I missed any).

Project left un-licensed (and thus copyrighted) until it actually does something.

## Notes

* Test album: https://photos.app.goo.gl/gcrtqKqLaxkz2jYcA

    * aka https://photos.google.com/share/AF1QipOsyTRCCkFhI8kRqZiQ8K5ICY_836mUn6wQNmiPRZUAxaGLGL4pMqylMVe04RNbDA?key=MktDaHBHQlNHSzFFdFo4WEVGZjRfbE9HUEFpRDNn
    * album ID `ABqBtt-Uyj3E7zHBYXRi3sZIu4tBJBwSbWMUNvxrEqtdFex-v4w7iY1La45w57rVt4QwGQjKW6fr`
    * image IDs
        * `ABqBtt-SUE55wIz-mgbWvFbiaR4xOXim8vg4B-6_G4xGYEB9qrMNATuYcBJIWGSLu3mrjy-OGMuje5Q4MwmuHVJ3divYtnJuaA`
        * `ABqBtt9yxrUmrvqghqdD4a5TGTDXze20qxX8ex9vtvVSSZGbVni4cSJarOjJRq_08LEn5oUSKDByvyn-jz7end7vGfJfm_SeyA`

* Longer album: https://photos.google.com/share/AF1QipPJW0gqaSFeTccPW6j2VdRm_5AG5RMzTtF14m433rPdZetpBLzmfQf4k-mdUrxULQ?key=Mk9QZ2tXY2h3WnhvMjBycUVYcldXR1JNMnY0ZTd3

Can't correlate info from API with info parsed from saved page, no IDs overlap

`AF_initDataCallback(<stuff here>)` seems to be a protobuf

* Another idea: breakpoint on something, see what the actual code is doing
* Another idea: manually saving as har file, using haralyzer package to work with it


### protobuf docs

overall structure

```
[
    null
    [list of images],
    "",
    [album info including sharing?],
    [list of enrichments]
]
```

list of images format - same order as display
```
[
    "AF1QipOlQgoYJGjKaFOMHJkYqQVH4zxkn9brxgwXHhq2", # Not the ID. part of productURL? seems stable-ish
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
    <date, unix epoch, photo taken>,
    "TOt7ob2rr6UBovGSirT8orZJDaM", # not the ID, but stable across requests & remove/re-add to album
    <tz offset, seconds, probably for date taken>,
    <date, unix epoch, added to album?>,
    [
        "AF1QipMN6zXOdB5TdqYqMm_qJ4Q0699P" # data-actor-media-key - google account that the image is from?
    ],
    [ # same in all images - possibly related to phone metadata?
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
    19222, # same in both images
    [],
    { # related to ordering
        "101428965": [
            0,
            "vdh9cohf070000000000004k" # all images end in 'k'
        ]
    }
],
```

list of enhancements format - order added?

* `99218341` = stable key for enrichment info
    * 1=text, 2=location, 3=map

text
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
                1,  # 1 = text
                [
                    "text to display"
                ]
            ]
        ],
        "101428965": [ # Ordering
            0,
            "vdh9cohf0700g0000000004a" # enrichments end in 'a'
        ]
    }
]
```

location
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
                2, # 2 = location
                null,
                [
                    null,
                    [
                        [
                            3, # location?
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
        "101428965": [ # Ordering
            0,
            "vdh9cohf06vv00000000004a" # enrichments end in 'a'
        ]
    }
],
```

map
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
                        [ # source location
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
                        [ # destination location
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
        "101428965": [ # Ordering
            0,
            "vdh9cohf06vto0000000004a" # enrichments end in 'a'
        ]
    }
],
```

### ordering notes

* `101428965` = ordering info? always has `[0, <similar string>]`
* similar string
    * same: `vdh9` appears repeatedly - possibly album prefix or encoding info that's the same for a given album
    * ends in `k` = image
    * ends in `a` = enrichment
    * often ends with `000000000004k` or `00000000004a`, possibly because very small album
        * large album has more variety in end
    * sometimes ending omitted eg `vdh9d3bi` vs `vdh9cohf070000000000004k` in the same album
        * or `vdcpo87k` vs `vdcpo87k06vt00000000004a`
* changing ordering changes 1 character in the string
    * item that was click-and-dragged is the one that changes
    * string seems to sort a > b, 1>2
    * aka naive sorting based on the strings works

### Images

3 image sizes?
* smallest = "baseURL"
* medium = "baseUrl" + "=d" also missing some metadata like GPS, shows as generated by Picasa
    * baseURL needs a suffix applied - "=d" for download (original? all exif except location metadata)
    * could specify "=w##-h##" to get that, still not original metadata
* largest = "productURL" -> go and download item from menu. Original? App can't open, only user?
* see also https://developers.google.com/photos/library/guides/access-media-items#base-urls


## Ref

### photos api

* https://pypi.org/project/gphotos-sync/ ref for how used?
* https://github.com/gilesknap/gphotos-sync/tree/master/gphotos
* https://developers.google.com/photos/library/guides/authentication-authorization
* https://developers.google.com/photos/library/guides/get-started
* https://developers.google.com/photos/library/guides/list#listing-album-contents
* https://developers.google.com/photos/library/reference/rest/v1/albums
* https://stackoverflow.com/questions/52281453/google-photos-api-with-filter-to-get-photos-with-album-information
* https://github.com/alexcrist/scrape-google-photos

### auth

* https://google-auth.readthedocs.io/en/latest/user-guide.html
* https://oauthlib.readthedocs.io/en/latest/oauth2/clients/client.html
* https://github.com/requests/requests-oauthlib
* https://requests-oauthlib.readthedocs.io/en/latest/examples/google.html
