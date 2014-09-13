

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

    function on_sensor_changed(args) {
        console.log('Event: on_sensor_changed received from sensor');
    }
    session.subscribe('io.github.si618.pi-time.on_sensor_changed', on_sensor_changed).then(
        function(sub) {
            console.log('Subscribed to: on_sensor_changed');
        },
        function(err) {
            console.log('Failed to subscribe to: on_sensor_changed ' + err);
        }
    );

    function on_sensor_event(args) {
        console.log('Event: on_sensor_event received from sensor');
    }
    session.subscribe('io.github.si618.pi-time.on_sensor_event', on_sensor_event).then(
        function(sub) {
            console.log('Subscribed to: on_sensor_event');
        },
        function(err) {
            console.log('Failed to subscribe to: on_sensor_event ' + err);
        }
    );

    function on_laptimer_changed(args) {
        console.log('Event: on_laptimer_changed received from laptimer');
    }
    session.subscribe('io.github.si618.pi-time.on_laptimer_changed', on_laptimer_changed).then(
        function(sub) {
            console.log('Subscribed to: on_laptimer_changed');
        },
        function(err) {
            console.log('Failed to subscribe to: on_laptimer_changed ' + err);
        }
    );

    function on_laptimer_heartbeat(args) {
        console.log('Event: on_laptimer_heartbeat received from laptimer');
    }
    session.subscribe('io.github.si618.pi-time.on_laptimer_heartbeat', on_laptimer_heartbeat).then(
        function(sub) {
            console.log('Subscribed to: on_laptimer_heartbeat');
        },
        function(err) {
            console.log('Failed to subscribe to: on_laptimer_heartbeat ' + err);
        }
    );

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
    console.log('Lost connection to sensor node: ' + reason);
}

connection.open();
