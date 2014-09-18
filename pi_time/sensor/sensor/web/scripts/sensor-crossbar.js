// Sesnor specific crossbar code

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

// Fired when connection is established and session attached
connection.onopen = function(session, details) {
    console.log('Connection to sensor opened');

    function sensor_changed(details) {
        console.log('TODO: [sensor_changed] Update sensor config view model...');
    }
    sessionSubscribe(session, 'sensor_changed', sensor_changed);

    function sensor_event(details) {
        console.log('TODO: [sensor_event] Update sensor event view model...');
    }
    sessionSubscribe(session, 'sensor_event', sensor_event);

    function laptimer_changed(details) {
        console.log('TODO: [laptimer_changed]');
    }
    sessionSubscribe(session, 'laptimer_changed', laptimer_changed);

    function laptimer_heartbeat(details) {
        console.log('TODO: [laptimer_heartbeat]');
    }
    sessionSubscribe(session, 'laptimer_heartbeat', laptimer_heartbeat);

    function sensor_options(details) {
        console.log('TODO: Update sensor options view model...');
    }
    sessionCall(session, 'get_sensor_options', [], sensor_options);

    function sensor_config(details) {
        console.log('TODO: Update sensor config view model...');
    }
    sessionCall(session, 'get_sensor_config', [], sensor_config);
    sensorVM.status.sensor(true);
};

connection.onclose = function(reason, details) {
    sensorVM.status.sensor(false);
    console.log('Connection to sensor closed: ' + reason);
}

connection.open();
