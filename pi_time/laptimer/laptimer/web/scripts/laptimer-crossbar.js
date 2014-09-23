// Laptimer specific crossbar code

function openSensorConnections(details) {
    // TODO: Add support for multiple sensors
    openSensorConnection(details);
}

function openSensorConnection(details) {
    var sensorConnection = getConnection(details.url);

    sensorConnection.onopen = function(session, detalis) {
        console.log('Connection to sensor opened');

        function sensor_started(details) {
            // TODO: Add support for multiple sensors
            console.log('[sensor_started]');
            mainVM.status.sensor(true);
        }
        sessionSubscribe(session, 'sensor_started', sensor_started);

        function sensor_stopped(details) {
            // TODO: Add support for multiple sensors
            console.log('[sensor_stopped]');
            mainVM.status.sensor(false);
        }
        sessionSubscribe(session, 'sensor_stopped', sensor_stopped);

        function sensor_changed(details) {
            // TODO: Add support for multiple sensors
            console.log('[sensor_changed] Update sensor settings');
        }
        sessionSubscribe(session, 'sensor_changed', sensor_changed);

        function sensor_event(details) {
            console.log('[sensor_event] Update sensor events');
        }
        sessionSubscribe(session, 'sensor_event', sensor_event);

        // TODO: Add support for multiple sensors
        mainVM.admin.status.sensor(true);
    };

    sensorConnection.onclose = function(reason, details) {
        // TODO: Add support for multiple sensors
        mainVM.admin.status.sensor(false);
        console.log('Connection to sensor closed (' + reason + ')');
    };

    sensorConnection.open();
}

var laptimerConnection = getConnection();

// Fired when connection is established and session attached
laptimerConnection.onopen = function(session, details) {
    console.log('Connection to laptimer opened');

    function laptimer_changed(details) {
        console.log('[laptimer_changed] Updating laptimer settings');
    }
    sessionSubscribe(session, 'laptimer_changed', laptimer_changed);

    sessionCall(session, 'get_sensor_config', null, openSensorConnections);

    mainVM.admin.status.laptimer(true);
};

laptimerConnection.onclose = function(reason, details) {
    mainVM.admin.status.laptimer(false);
    console.log('Connection to laptimer closed (' + reason + ')');
};

laptimerConnection.open();
