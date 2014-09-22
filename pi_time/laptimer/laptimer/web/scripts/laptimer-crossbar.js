// Laptimer specific crossbar code

var connection = getConnection();

// Fired when connection is established and session attached
connection.onopen = function(session, details) {
    console.log('Connection to laptimer opened');

    function laptimer_changed(details) {
        console.log('TODO: [laptimer_changed]');
    }
    sessionSubscribe(session, 'laptimer_changed', laptimer_changed);

    function sensor_started(details) {
        console.log('TODO: [sensor_started] Update sensor config view model...');
    }
    sessionSubscribe(session, 'sensor_started', sensor_started);

    function sensor_changed(details) {
        console.log('TODO: [sensor_changed]');
    }
    sessionSubscribe(session, 'sensor_changed', sensor_changed);

    function sensor_event(details) {
        console.log('TODO: [sensor_event]');
    }
    sessionSubscribe(session, 'sensor_event', sensor_event);

    function sensor_connected(details) {
        // TODO: Support multiple sensors
        // mainVM.admin.status.sensor(true);
        console.log('TODO: [sensor_connected]' + details);
    }
    sessionSubscribe(session, 'sensor_connected', sensor_connected);

    sessionCall(session, 'laptimer_started').then(
        function laptimer_started(result) {
            mainVM.admin.status.laptimer(true);
        }
    );
};

connection.onclose = function(reason, details) {
    mainVM.admin.status.laptimer(false);
    console.log('Connection to laptimer closed (' + reason + ')');
};

connection.open();
