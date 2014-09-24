// Sensor specific crossbar code

function startSensor(vm) {
    var sensor = getConnection();

    sensor.onopen = function(session, details) {
        console.log('Connection to sensor opened');

        function sensorChanged(details) {
            console.log('[sensor_changed] Update sensor settings');
        }
        sessionSubscribe(session, 'sensor_changed', sensorChanged);

        function sensorTriggered(details) {
            console.log('Event sensor_triggered (' + details + ')');
            vm.status.triggered(true);
            setTimeout(function() {
                vm.status.triggered(false);
            }, 1000);
        }
        sessionSubscribe(session, 'sensor_triggered', sensorTriggered);

        function laptimerConfig(details) {
            vm.settings.laptimerName(details.name);
            vm.settings.laptimerUrl(details.url);
            startLaptimer(details);
        }
        sessionCall(session, 'get_laptimer_config', null, laptimerConfig);

        function sensorConfig(details) {
            vm.settings.sensorName(details[0].name);
            vm.settings.sensorUrl(details[0].url);
            vm.settings.hardware(details[0].hardware);
            vm.settings.location(details[0].location);
        }
        sessionCall(session, 'get_sensor_config', null, sensorConfig);

        vm.status.sensor(true);
    };

    sensor.onclose = function(reason, details) {
        vm.status.sensor(false);
        console.log('Connection to sensor closed (' + reason + ')');
    };

    sensor.open();

    // Nested function to preserve scope allowing update of view model observables
    function startLaptimer(details) {
        var laptimer = getConnection(details.url);

        laptimer.onopen = function(session, detalis) {
            console.log('Connection to laptimer opened');

            function laptimerStarted(details) {
                console.log('[laptimer_started]');
                vm.status.laptimer(true);
            }
            sessionSubscribe(session, 'laptimer_started', laptimerStarted);

            function laptimerStopped(details) {
                console.log('[laptimer_stopped]');
                vm.status.laptimer(false);
            }
            sessionSubscribe(session, 'laptimer_stopped', laptimerStopped);

            function laptimerChanged(details) {
                console.log('[laptimer_changed] Update laptimer settings');
            }
            sessionSubscribe(session, 'laptimer_changed', laptimerChanged);

            function lapStarted(details) {
                console.log('[lap_started]');
                vm.status.lap(true);
            }
            sessionSubscribe(session, 'lapStarted', lapStarted);

            function lapFinished(details) {
                console.log('[lap_finished]');
                vm.status.lap(false);
            }
            sessionSubscribe(session, 'lap_finished', lapFinished);

            function lapCancelled(details) {
                console.log('[lap_cancelled]');
                vm.status.lap(false);
            }
            sessionSubscribe(session, 'lap_cancelled', lapCancelled);

            vm.status.laptimer(true);
        };

        laptimer.onclose = function(reason, details) {
            vm.status.laptimer(false);
            console.log('Connection to laptimer closed (' + reason + ')');
        };

        laptimer.open();
    }
}
