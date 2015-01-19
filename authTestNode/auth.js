authSessions = {}

function RequestAuthenticator(server, appID) {
	this.server = server;
	this.appID = appID;

	this.setAuthCookie = undefined;
	this.getAuthCookie = undefined;
	this.redirectFunction = undefined;
	this.returnURL = undefined;

	Object.defineProperty(this, 'isAuthenticated', {
	    get: function() {
	        authCookie = this.getAuthCookie();
	        return (authCookie in authSessions)
	    }
	});

	Object.defineProperty(this, 'user', {
	    get: function() {
	    	if (!this.isAuthenticated)
	    		return false;

	        authCookie = this.getAuthCookie();
	        return authSessions[authCookie];
	    }
	});
}

RequestAuthenticator.prototype.authenticate = function() {
	if (this.isAuthenticated)
		return true;

	//we know the auth sessionID hasnt come back yet because
	//that gets called before this function
	if (typeof this.returnURL == "undefined") {
		throw new Error("requestAuthenticator.returnURL not set");
		return false;
	}

	this.redirectFunction("http://" + this.server + "/login?returnURL=" + encodeURIComponent(this.returnURL))
	return undefined
}

RequestAuthenticator.prototype.handleAuthSessionID = function(authSessionID, callback) {
	if (this.isAuthenticated) {
		callback(true);
		return
	}

	//validate authSessionID
	validateHost = this.server
	validatePath = "/validateSession?authSessionID="+encodeURIComponent(authSessionID)
	if (typeof(this.appID) == "undefined") {
		validatePath += "&appID=" + encodeURIComponent(this.appID)
	}
	var self = this;
	request(validateHost, validatePath, function(validateSessionReply){
		validateSessionReply = JSON.parse(validateSessionReply)
		if (validateSessionReply['authenticated'] == true) {
			authSessionCookieID = makeid()
			authSessions[authSessionCookieID] =	{
				 'userID': validateSessionReply['userID']
				,'username': validateSessionReply['username']
			}

			self.setAuthCookie(authSessionCookieID)
			self.getAuthCookie = function(){return authSessionCookieID};
			self.redirectFunction(self.returnURL)
			callback(false);
		}
	});	
}

RequestAuthenticator.prototype.logout = function() {
	this.setAuthCookie("")
	this.redirectFunction("http://" + this.server + "/logout?returnURL=" + encodeURIComponent(this.returnURL))
	return !this.isAuthenticated
}

module.exports.RequestAuthenticator = RequestAuthenticator;



function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 15; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

function request(host, path, cb) {
	var http = require('http');
	var options = {
		host: host,
		path: path
	};

	callback = function(response) {
		var str = '';

		//another chunk of data has been recieved, so append it to `str`
		response.on('data', function (chunk) {
			str += chunk;
		});
		//the whole response has been recieved, so we just print it out here
		response.on('end', function () {
			cb(str);
		});
	};

	http.request(options, callback).end();
}