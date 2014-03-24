# Load the http module to create an http server.
HOST  = 'https://api.wrapp.com'
http  = require 'http'
https = require 'https'

port = 8080

server = http.createServer (request, response) ->
	console.log 'hit: ' + request.url
	if not overrideInput(request.url, response)
		https.get(HOST + request.url, (res) =>
			response.writeHead res.statusCode, res.headers
			output = ''
			res.on 'data', (d) =>
				output += d
			res.on 'end', =>
				response.end output
		).on('error', (e) =>
			console.log e
		)
	else
		response.writeHead 200, { 'Content-Type': 'text/plain' }


server.listen port

console.log "Server running at http://127.0.0.1:#{port}/"


overrideInput = (url, response) ->
	if url.indexOf('/users/me/news') != -1
		response.end JSON.stringify(news)
		return true
	false


news =
    status: 'ok'
    news: [
        {
            gift_id     : 'r3X7S1PY'
            image       : 'http://graph.facebook.com/540915851/picture'
            uri         : 'wrappcorp:///gifts/r3X7S1PY'
            create_time : '2014-03-20T19:48:56+0000'
            message     : 'You wrapped a gift for Mikael A.'
            type        : 'notification'
            id          : 13
        }
        {
            gift_id     : '7hgDHsSX'
            image       : 'http://graph.facebook.com/598632743/picture'
            create_time : '2014-03-19T17:05:27+0000'
            message     : 'C\u00e9sar P wrapped a gift for Cesar.'
            type        : 'notification'
            id          : 11
        }
    ]
