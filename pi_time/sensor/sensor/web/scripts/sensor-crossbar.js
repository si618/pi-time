// Sensor specific crossbar code

var connection = getConnection();

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

    function laptimer_connected(details) {
        mainVM.status.laptimer(true);
    }
    sessionSubscribe(session, 'laptimer_connected', laptimer_connected);

    function laptimer_disconnected(details) {
        mainVM.status.laptimer(false);
    }
    sessionSubscribe(session, 'laptimer_disconnected', laptimer_disconnected);

    function laptimer_changed(details) {
        console.log('TODO: [laptimer_changed]');
    }
    sessionSubscribe(session, 'laptimer_changed', laptimer_changed);

    function laptimer_heartbeat(details) {
        console.log('TODO: [laptimer_heartbeat]');
    }
    sessionSubscribe(session, 'laptimer_heartbeat', laptimer_heartbeat);

    function sensor_started(result) {
        mainVM.status.sensor(true);
        // TODO: Wire up settings options and sensor config
    }
    sessionCall(session, 'sensor_started', null, sensor_started);
};

connection.onclose = function(reason, details) {
    mainVM.status.sensor(false);
    console.log('Connection to sensor closed (' + reason + ')');
};

connection.open();
