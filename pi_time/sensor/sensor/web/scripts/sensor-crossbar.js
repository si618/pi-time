// Sensor specific crossbar code

function openLaptimerConnection(details) {
    var laptimerConnection = getConnection(details.url);

    laptimerConnection.onopen = function(session, detalis) {
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

        mainVM.status.laptimer(true);
    };

    laptimerConnection.onclose = function(reason, details) {
        mainVM.status.laptimer(false);
        console.log('Connection to laptimer closed (' + reason + ')');
    };

    laptimerConnection.open();
}

var sensorConnection = getConnection();

sensorConnection.onopen = function(session, details) {
    console.log('Connection to sensor opened');

    function sensor_changed(details) {
        console.log('[sensor_changed] Update sensor settings');
    }
    sessionSubscribe(session, 'sensor_changed', sensor_changed);

    function sensor_event(details) {
        console.log('[sensor_event] Update sensor events');
    }
    sessionSubscribe(session, 'sensor_event', sensor_event);

    mainVM.status.sensor(true);

    sessionCall(session, 'get_laptimer_config', null, openLaptimerConnection);
};

sensorConnection.onclose = function(reason, details) {
    mainVM.status.sensor(false);
    console.log('Connection to sensor closed (' + reason + ')');
};

sensorConnection.open();
