var auth = require('./auth');

function getAuth(req, res, callback){
	var authHandler = new auth.RequestAuthenticator("auth.jyelewis.com", "com.jyelewis.testing");
	authHandler.setAuthCookie = function(value) { res.cookie('testAuth', value); }
	authHandler.getAuthCookie = function() { return req.cookies['testAuth']; }

	authHandler.redirectFunction = function(url) { res.redirect(url); }
	authHandler.returnURL = "http://localhost:3000"

	if ("authSessionID" in req.query) {
		authHandler.handleAuthSessionID(req.query["authSessionID"], function(isAuthed) {
			if (isAuthed)
				callback(authHandler); //do not callback, page is reloaded
			else
				res.end();
		});
		return
	}

	if (typeof(authHandler.authenticate()) == "undefined") {
		return //never call the callback
		res.end();
	}

	callback(authHandler.isAuthenticated ? authHandler : false)
}


//server stuff
var express = require('express')
var app = express()

app.use(express.cookieParser());

app.get('/', function (req, res) {
	getAuth(req, res, function(currAuth){
		if (currAuth) {
			res.end("Hello, " + currAuth.user['username'])
		} else if (currAuth == false) {
			console.log("denied")
			res.end("403: Access denied")
		}
	});
});

app.get('/logout', function (req, res) {
	getAuth(req, res, function(currAuth){
		if (currAuth) {
			currAuth.logout();
		} else if (currAuth == false) {
			res.redirect("/")
		}
	});
});

var server = app.listen(3000, function () {

  var host = server.address().address
  var port = server.address().port

  console.log('Example app listening at http://%s:%s', host, port)

})