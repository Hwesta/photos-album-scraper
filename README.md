# Readme

## Problem

Export of Google Photos albums sucks. Google Takeout only does photos. The [API](https://developers.google.com/photos/library/reference/rest/v1/albums/) only returns name and cover information, and no part of the API returns "enrichments" like text and locations, with [no plans to add that](https://issuetracker.google.com/issues/129050144). The page returned from a HTTP request or to the browser is unreadable JS garbage, with all the functions minified and the content in obtuse data strings.

## Goal

Write a script that can export a Google Photos album into human-readable HTML, CSS and Javascript that I can host anywhere.

I couldn't find any projects that did this already (but please let me know if I missed any).

Project left un-licensed (and thus copyrighted) until it actually does something.
