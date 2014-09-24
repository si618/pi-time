// Laptimer specific crossbar code

function startLaptimer(vm) {
    var laptimer = getConnection();

    // Fired when connection is established and session attached
    laptimer.onopen = function(session, details) {
        console.log('Connection to laptimer opened');

        function laptimer_changed(details) {
            console.log('[laptimer_changed] Updating laptimer settings');
        }
        sessionSubscribe(session, 'laptimer_changed', laptimer_changed);

        sessionCall(session, 'get_sensor_config', null, startSensors);

        vm.admin.status.laptimer(true);
    };

    laptimer.onclose = function(reason, details) {
        vm.admin.status.laptimer(false);
        console.log('Connection to laptimer closed (' + reason + ')');
    };

    laptimer.open();

    function startSensors(details) {
        // TODO: Add support for multiple sensors - foreach sensor in details...
        startSensor(details);
    }

    // Nested function to preserve scope allowing update of view model observables
    function startSensor(details) {
        var sensor = getConnection(details.url);

        sensor.onopen = function(session, detalis) {
            console.log('Connection to sensor opened');

            function sensor_started(details) {
                console.log('[sensor_started]');
                // TODO: Add support for multiple sensors
                //vm.admin.status.sensor(true);
            }
            sessionSubscribe(session, 'sensor_started', sensor_started);

            function sensor_stopped(details) {
                console.log('[sensor_stopped]');
                // TODO: Add support for multiple sensors
                //vm.admin.status.sensor(false);
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
            //vm.admin.status.sensor(true);
        };

        sensor.onclose = function(reason, details) {
            // TODO: Add support for multiple sensors
            //vm.admin.status.sensor(false);
            console.log('Connection to sensor closed (' + reason + ')');
        };

        sensor.open();
    }
}
