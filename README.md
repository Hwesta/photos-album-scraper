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

* Longer album: https://photos.google.com/share/AF1QipPJW0gqaSFeTccPW6j2VdRm_5AG5RMzTtF14m433rPdZetpBLzmfQf4k-mdUrxULQ?key=Mk9QZ2tXY2h3WnhvMjBycUVYcldXR1JNMnY0ZTd3



## Ref

### photos api

* https://pypi.org/project/gphotos-sync/ ref for how used?
* https://github.com/gilesknap/gphotos-sync/tree/master/gphotos
* https://developers.google.com/photos/library/guides/authentication-authorization
* https://developers.google.com/photos/library/guides/get-started
* https://developers.google.com/photos/library/guides/list#listing-album-contents
* https://developers.google.com/photos/library/reference/rest/v1/albums
* https://stackoverflow.com/questions/52281453/google-photos-api-with-filter-to-get-photos-with-album-information

### auth

* https://google-auth.readthedocs.io/en/latest/user-guide.html
* https://oauthlib.readthedocs.io/en/latest/oauth2/clients/client.html
* https://github.com/requests/requests-oauthlib
* https://requests-oauthlib.readthedocs.io/en/latest/examples/google.html
