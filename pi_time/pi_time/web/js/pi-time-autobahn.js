// Pi-time autobahn scripts shared between laptimer and sensor

function printError(error) {
    var msg = error.error;
    if (AUTOBAHN_DEBUG === true && error.args.length > 0) {
        msg += ": " + error.args[0];
    }
    return msg;
}

// Helper function to subscribe to an autobahn event
function subscribe(name, method, success, failure) {
    session.subscribe(URI_PREFIX + name, method).then(
        function (sub) {
            console.log("Subscribed to " + name);
            if (success !== undefined) {
                success(sub);
            }
        },
        function (err) {
            console.log("Failed to subscribe to " + name +
                " (" + printError(err) + ")");
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
function rpc(procedure, callback, options) {
    var params = options ? (options.params ? options.params : []) : [];
    if (session === null || !session.isOpen) {
        console.log("Unable to call " + procedure + " (session closed)");
    }
    console.log("Request " + procedure);
    session.call(URI_PREFIX + procedure, params).then(
        function (res) {
            console.log("Response from " + procedure + " (ok)");
            if (callback) {
                callback(res);
            }
        },
        function (err) {
            console.log("Response from " + procedure + " (" + printError(err) + ")");
            if (options.failure) {
                options.failure(err);
            }
        }
    );
}

function getConnection() {
    // URL of WAMP Router (Crossbar.io)
    var protocol = document.location.protocol === "http:" ? "ws:" : "wss:";
    var wsuri = protocol + "//" + document.location.host + "/ws";
    // WAMP connection to Router
    return new autobahn.Connection({
        url: wsuri,
        realm: "pi-time"
    });
}
