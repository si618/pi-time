// Sensor specific crossbar code

function startLaptimer(details) {
    var connection = getConnection(details.url);

    connection.onopen = function(session, detalis) {
        console.log('Connection to laptimer opened');

        function laptimer_started(details) {
            console.log('[laptimer_started]');
            mainVM.status.laptimer(true);
        }
        sessionSubscribe(session, 'laptimer_started', laptimer_started);

        function laptimer_stopped(details) {
            console.log('[laptimer_stopped]');
            mainVM.status.laptimer(false);
        }
        sessionSubscribe(session, 'laptimer_stopped', laptimer_stopped);

        function laptimer_changed(details) {
            console.log('[laptimer_changed] Update laptimer settings');
        }
        sessionSubscribe(session, 'laptimer_changed', laptimer_changed);

        function lap_started(details) {
            console.log('[lap_started]');
            mainVM.status.lap(true);
        }
        sessionSubscribe(session, 'lap_started', lap_started);

        function lap_finished(details) {
            console.log('[lap_finished]');
            mainVM.status.lap(false);
        }
        sessionSubscribe(session, 'lap_finished', lap_finished);

        function lap_cancelled(details) {
            console.log('[lap_cancelled]');
            mainVM.status.lap(false);
        }
        sessionSubscribe(session, 'lap_cancelled', lap_cancelled);

        mainVM.status.laptimer(true);
    };

    connection.onclose = function(reason, details) {
        mainVM.status.laptimer(false);
        console.log('Connection to laptimer closed (' + reason + ')');
    };

    connection.open();
}

function startSensor() {
    var connection = getConnection();

    connection.onopen = function(session, details) {
        console.log('Connection to sensor opened');

        function sensor_changed(details) {
            console.log('[sensor_changed] Update sensor settings');
        }
        sessionSubscribe(session, 'sensor_changed', sensor_changed);

        function sensor_triggered(details) {
            console.log('Event sensor_triggered (' + details +')');
            mainVM.status.triggered(true);
            setTimeout(function() {
                mainVM.status.triggered(false);
            }, 1000);
        }
        sessionSubscribe(session, 'sensor_triggered', sensor_triggered);

        sessionCall(session, 'get_laptimer_config', null, startLaptimer);

        mainVM.status.sensor(true);
    };

    connection.onclose = function(reason, details) {
        mainVM.status.sensor(false);
        console.log('Connection to sensor closed (' + reason + ')');
    };

    connection.open();
}

startSensor();
