// Autobahn specific code for sensor web app

function openSensorConnection() {

    connection = getConnection();

    connection.onopen = function (connectionSession, details) {
        session = connectionSession;

        subscribe("sensor_changed", sensorChanged);
        subscribe("sensor_triggered", sensorTriggered);

        subscribe("laptimer_started", laptimerStarted);
        subscribe("laptimer_stopped", laptimerStopped);
        subscribe("laptimer_changed", laptimerChanged);

        subscribe("lap_started", lapStarted);
        subscribe("lap_finished", lapFinished);
        subscribe("lap_cancelled", lapCancelled);

        connectionOpened(details);
    };

    connection.onclose = function (reason, details) {
        connectionClosed(reason, details);
    };

    connection.open();
}

openSensorConnection();
