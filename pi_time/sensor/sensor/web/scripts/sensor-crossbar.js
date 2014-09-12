

// URL of WAMP Router (Crossbar.io)
var wsuri;
if (document.location.origin == 'file://') {
    wsuri = 'ws://127.0.0.1:8888/ws';

} else {
    wsuri = (document.location.protocol === 'http:' ? 'ws:' : 'wss:') + '//' +
        document.location.host + '/ws';
}

// WAMP connection to Router
var connection = new autobahn.Connection({
    url: wsuri,
    realm: 'pi-time'
});

// fired when connection is established and session attached
connection.onopen = function(session, details) {

    console.log('Connected to sensor node');

/*
    function on_laptimerevent(args) {
        var laptimer = args[0];
        // TODO: laptimer contain details of status change of laptimer
        // server (start/stop/error) or current lap (started/finished)
        console.log('Event: on_laptimerevent received from laptimer ' + laptimer);
    }
    session.subscribe('io.github.si618.pi-time.onlaptimerevent', on_laptimerevent).then(
        function(sub) {
            console.log('Subscribed to: onlaptimerevent');
        },
        function(err) {
            console.log('Failed to subscribe to: onlaptimerevent ' + err);
        }
    );

    function on_sensorevent(args) {
        var sensor = args[0];
        var occured = args[1]
        console.log('Event: on_sensorevent received from sensor ' + sensor);
    }
    session.subscribe('io.github.si618.pi-time.onsensorevent', on_sensorevent).then(
        function(sub) {
            console.log('Subscribed to: onsensorevent');
        },
        function(err) {
            console.log('Failed to subscribe to: onsensorevent ' + err);
        }
    );
*/

    session.call('io.github.si618.pi-time.get_sensor_options').then(
        function(res) {
            /* TODO: Update view model */
            console.log("API response 'get_sensor_options' (ok)");
        },
        function(err) {
            console.log("API response 'get_sensor_options' error " + err);
        }
    );

    session.call('io.github.si618.pi-time.get_sensor_config').then(
        function(res) {
            /* TODO: Update view model */
            console.log("API response 'get_sensor_config' (ok)");
        },
        function(err) {
            console.log("API response 'get_sensor_config' error " + err);
        }
    );
};

connection.onclose = function(reason, details) {
    console.log('Connection to sensor node lost: ' + reason);
}

connection.open();
