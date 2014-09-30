// Autobahn specific code for laptimer web app

function startSensor(details) {
    var connection = getConnection(details.url);

    connection.onopen = function(session, detalis) {
        console.log('Connection to sensor opened');

        function sensor_started(details) {
            console.log('[sensor_started]');
            // TODO: Add support for multiple sensors
            //vm.admin.status.sensor(true);
        }
        subscribe(session, 'sensor_started', sensor_started);

        function sensor_stopped(details) {
            console.log('[sensor_stopped]');
            // TODO: Add support for multiple sensors
            //vm.admin.status.sensor(false);
        }
        subscribe(session, 'sensor_stopped', sensor_stopped);

        function sensor_changed(details) {
            // TODO: Add support for multiple sensors
            console.log('[sensor_changed] Update sensor settings');
        }
        subscribe(session, 'sensor_changed', sensor_changed);

        function sensor_event(details) {
            console.log('[sensor_event] Update sensor events');
        }
        subscribe(session, 'sensor_event', sensor_event);

        // TODO: Add support for multiple sensors
        //vm.admin.status.sensor(true);
    };

    connection.onclose = function(reason, details) {
        // TODO: Add support for multiple sensors
        //vm.admin.status.sensor(false);
        console.log('Connection to sensor closed (' + reason + ')');
    };

    connection.open();

    return connection;
}

function startLaptimer() {
    var connection = getConnection();

    // Fired when connection is established and session attached
    connection.onopen = function(session, details) {
        console.log('Connection to laptimer opened');

        function laptimer_changed(details) {
            console.log('[laptimer_changed] Updating laptimer settings');
        }
        subscribe(session, 'laptimer_changed', laptimer_changed);

        function startSensors(details) {
            // TODO: Add support for multiple sensors - foreach sensor in details...
            vm.sensorConnection.push(startSensor(details));
        }
        rpc('get_sensor_config', startSensors);

        vm.admin.status.laptimer(true);
    };

    connection.onclose = function(reason, details) {
        vm.admin.status.laptimer(false);
        console.log('Connection to laptimer closed (' + reason + ')');
    };

    connection.open();

    return connection;
}

vm.connection = startLaptimer();
