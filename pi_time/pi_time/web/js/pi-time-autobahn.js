// Pi-time autobahn scripts shared between laptimer and sensor

function printError(error) {
    msg = error.error;
    if (AUTOBAHN_DEBUG === true && error.args.length > 0) {
        msg += ': ' + error.args[0];
    }
    return msg;
}


// Helper function to subscribe to an autobahn event
function subscribe(name, method, success, failure) {
    session.subscribe(URI_PREFIX + name, method).then(
        function(sub) {
            console.log('Subscribed to ' + name);
            if (success !== undefined) {
                success(sub);
            }
        },
        function(err) {
            console.log('Failed to subscribe to ' + name +
                ' (' + printError(err) + ')');
            if (failure !== undefined) {
                failure(err);
            }
        }
    );
}

// Helper function to invoke to an autobahn rpc call. Options are:
//   session: Name of session, otherwise use default vm.connection.session
//   params: RPC parameters, otherwise, pass none
//   failure: Name of function to call if unsuccessfull
function rpc(method, callback, options) {
    var params = options ? (options.params ? options.params : []) : [];
    if (session === null || !session.isOpen) {
        console.log('Unable to call ' + method + ' (session closed)');
    }
    console.log('Request ' + method);
    session.call(URI_PREFIX + method, params).then(
        function(res) {
            console.log('Response from ' + method + ' (ok)');
            if (callback) {
                callback(res);
            }
        },
        function(err) {
            console.log('Response from ' + method + ' (' + printError(err) + ')');
            if (options.failure) {
                options.failure(err);
            }
        }
    );
}

// Helper function to invoke to an autobahn rpc call.
function rpc2(method, params) {
    var deferred = new $.Deferred();
    // TODO: Call getConnection()) if connection === null?
    // TODO: Call connection.open() if connection.session === null || !connection.session.isOpen?
    if (connection === null || connection.session === null || !connection.session.isOpen) {
        error = 'Unable to call ' + method + ' (session closed)';
        console.log(error);
        deferred.reject(error);
    } else {
        console.log('Request ' + method);
        session.call(URI_PREFIX + method, params).then(
            function(res) {
                console.log('Response from ' + method + ' (ok)');
                deferred.resolve(res);
            },
            function(err) {
                console.log('Response from ' + method + ' (' + printError(err) + ')');
                deferred.reject(err);
            }
        );
    }
    return deferred.promise();
}

function getConnection() {
    // URL of WAMP Router (Crossbar.io)
    protocol = document.location.protocol === 'http:' ? 'ws:' : 'wss:';
    wsuri = protocol + '//' + document.location.host + '/ws';
    // WAMP connection to Router
    return new autobahn.Connection({
        url: wsuri,
        realm: 'pi-time'
    });
}
