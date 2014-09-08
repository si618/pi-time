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

    function getSensorEvents(args) {
        var sensor = args[0];
        var events = args[1];
        console.log('Got sensor events');
    }
    session.register('io.github.si618.pi-time.getSensorEvents', getSensorEvents).then(
        function(reg) {
            console.log('Registered procedure: getSensorEvents');
        },
        function(err) {
            console.log('Failed to register procedure: getSensorEvents ' + err);
        }
    );

    function getSensorConfig(args) {
        var hardware = args[0];
        var laptimerUrl = args[1];
        var sensorPosition = args[2];
        var sendorConfig = args[3]
        console.log('Got sensor config');
    }
    session.register('io.github.si618.pi-time.getSensorConfig', getSensorConfig).then(
        function(reg) {
            console.log('Registered procedure: getSensorConfig');
        },
        function(err) {
            console.log('Failed to register procedure: getSensorConfig ' + err);
        }
    );

    function setSensorConfig(setup) {
        session.call('io.github.si618.pi-time.setSensorConfig', [setup]).then(
            function(res) {
                console.log('Result from setSensorConfig:', res);
            },
            function(err) {
                console.log('Error from setSensorConfig: ', err);
            }
        );
    }
};

// fired when connection was lost (or could not be established)
connection.onclose = function(reason, details) {
    console.log('Connection to sensor node lost: ' + reason);
}

connection.open();
