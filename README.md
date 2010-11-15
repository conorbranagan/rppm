Radio Paradise Playlist Maker (RPPM)

This is a small, simple app created using the Django framework. The app scrapes the latest playlist data from http://radioparadise.com/ and adds any new songs to the RPPM database from which you can create playlists that you can purchase on iTunes.

Additional Details:
	* Setup requires having the server request /cron/scrape/ every 5 minutes or so to get the latest information
	* The main page is almost completely dynamic, with the playlist being updated on the fly with JS and the song listings be pulled through AJAX calls.
	* The final playlist page simply gives a list of the songs you've given with links to purchase them from iTunes
	* The app also generates a URL for every playlist so that you can access it in the future

Stuff used:
	* Python
	* The Django Framework
	* JS/jQuery
	* CSS
	* Apple's iTunes Music Store JSON API.
	