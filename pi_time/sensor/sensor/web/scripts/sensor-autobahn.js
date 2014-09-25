// Autobahn specific code for sensor web app

function startLaptimer(details) {
    var connection = getConnection(details.url);

    connection.onopen = function(session, detalis) {
        console.log('Connection to laptimer opened');

        function laptimerStarted(details) {
            console.log('[laptimer_started]');
            vm.status.laptimer(true);
        }
        subscribe(session, 'laptimer_started', laptimerStarted);

        function laptimerStopped(details) {
            console.log('[laptimer_stopped]');
            vm.status.laptimer(false);
        }
        subscribe(session, 'laptimer_stopped', laptimerStopped);

        function laptimerChanged(details) {
            console.log('[laptimer_changed] Update laptimer settings');
        }
        subscribe(session, 'laptimer_changed', laptimerChanged);

        function lapStarted(details) {
            console.log('[lap_started]');
            vm.status.lap(true);
        }
        subscribe(session, 'lapStarted', lapStarted);

        function lapFinished(details) {
            console.log('[lap_finished]');
            vm.status.lap(false);
        }
        subscribe(session, 'lap_finished', lapFinished);

        function lapCancelled(details) {
            console.log('[lap_cancelled]');
            vm.status.lap(false);
        }
        subscribe(session, 'lap_cancelled', lapCancelled);

        vm.status.laptimer(true);
    };

    connection.onclose = function(reason, details) {
        vm.status.laptimer(false);
        console.log('Connection to laptimer closed (' + reason + ')');
    };

    connection.open();

    return connection;
}

function startSensor() {
    var connection = getConnection();

    connection.onopen = function(session, details) {
        console.log('Connection to sensor opened');

        function sensorChanged(details) {
            console.log('[sensor_changed] Update sensor settings');
        }
        subscribe(session, 'sensor_changed', sensorChanged);

        function sensorTriggered(details) {
            console.log('Event sensor_triggered (' + details + ')');
            vm.status.triggered(true);
            setTimeout(function() {
                vm.status.triggered(false);
            }, 1000);
        }
        subscribe(session, 'sensor_triggered', sensorTriggered);

        function laptimerConfig(details) {
            vm.settings.laptimerName(details.name);
            vm.settings.laptimerUrl(details.url);
            vm.laptimerConnection = startLaptimer(details);
        }
        rpc('get_laptimer_config', laptimerConfig, {
            'session': session
        });

        function sensorConfig(details) {
            sensor = details[0];
            vm.settings.sensorName(sensor.name);
            vm.settings.sensorUrl(sensor.url);
            vm.settings.hardware(sensor.hardware);
            vm.settings.location(sensor.location);
        }
        rpc('get_sensor_config', sensorConfig, {
            'session': session
        });

        vm.status.sensor(true);
    };

    connection.onclose = function(reason, details) {
        vm.status.sensor(false);
        console.log('Connection to sensor closed (' + reason + ')');
    };

    connection.open();

    return connection;
}

vm.connection = startSensor();
