// Pi-time crossbar scripts shared between laptimer and sensor

URI_PREFIX = 'pi-time.';

// Helper function to subscribe to an autobahn event
function sessionSubscribe(session, name, method, success, failure) {
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

// Helper function to invoke to an autobahn rpc call
function sessionCall(session, method, params, success, failure) {
    console.log('Request ' + method);
    session.call(URI_PREFIX + method, params).then(
        function(res) {
            console.log('Response from ' + method + ' (ok)');
            if (success !== undefined) {
                success(res);
            }
        },
        function(err) {
            console.log('Response from ' + method + ' (' + printError(err) + ')');
            if (failure !== undefined) {
                failure(err);
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
