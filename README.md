# Readme

## Problem

Export of Google Photos albums sucks. Google Takeout only does photos. The [API](https://developers.google.com/photos/library/reference/rest/v1/albums/) only returns name and cover information, and no part of the API returns "enrichments" like text and locations, with [no plans to add that](https://issuetracker.google.com/issues/129050144). The page returned from a HTTP request or to the browser is unreadable JS garbage, with all the functions minified and the content in obtuse data strings.

## Goal

Write a script that can export a Google Photos album into human-readable HTML and locally stored images.

## Installation

I wrote this for myself, so the installation assumes you have a Python development environment. Only tested on Python 3.10

1. Checkout repo
1. `pipenv install`
1. `pipenv run ./scraper.py`

## Running

Typical usage: `pipenv run ./scraper.py --fetch <URL> --download --render --output-directory <PATH>`

`--fetch` fetches the album info from a public URL and parses it.  \
`--download` downloads all images in the album to `output-directory`.  \
`--render` creates a HTML page with all the images, text and maps in `output-directory`.

Further options are available with `-h` or `--help`
