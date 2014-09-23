// Laptimer specific crossbar code

function configureSensors(details) {
    // TODO: Add support for multiple sensors
    configureSensor(details);
}

function configureSensor(details) {
    var connection = getConnection(details.url);

    connection.onopen = function(session, detalis) {
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

    connection.onclose = function(reason, details) {
        // TODO: Add support for multiple sensors
        mainVM.admin.status.sensor(false);
        console.log('Connection to sensor closed (' + reason + ')');
    };

    connection.open();
}

function configureLaptimer() {
    var connection = getConnection();

    // Fired when connection is established and session attached
    connection.onopen = function(session, details) {
        console.log('Connection to laptimer opened');

        function laptimer_changed(details) {
            console.log('[laptimer_changed] Updating laptimer settings');
        }
        sessionSubscribe(session, 'laptimer_changed', laptimer_changed);

        sessionCall(session, 'get_sensor_config', null, configureSensors);

        mainVM.admin.status.laptimer(true);
    };

    connection.onclose = function(reason, details) {
        mainVM.admin.status.laptimer(false);
        console.log('Connection to laptimer closed (' + reason + ')');
    };

    laptimerConnection.open();
}

configureLaptimer();
