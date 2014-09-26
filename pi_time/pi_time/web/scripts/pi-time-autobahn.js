// Pi-time autobahn scripts shared between laptimer and sensor

URI_PREFIX = 'pi-time.';

function printError(error) {
    msg = error.error;
    if (AUTOBAHN_DEBUG === true && error.args.length > 0) {
        msg += ': ' + error.args[0];
    }
    return msg;
}


// Helper function to subscribe to an autobahn event
function subscribe(session, name, method, success, failure) {
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
    var session = options.session ? options.session : vm.connection.session;
    var params = options.params ? options.params : [];
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
function getConnection(wsuri) {
    // URL of WAMP Router (Crossbar.io)
    if (wsuri === undefined) {
        protocol = document.location.protocol === 'http:' ? 'ws:' : 'wss:';
        wsuri = protocol + '//' + document.location.host + '/ws';
    }
    // WAMP connection to Router
    var connection = new autobahn.Connection({
        url: wsuri,
        realm: 'pi-time'
    });
    return connection;
}
