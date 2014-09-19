// Laptimer specific crossbar code

var connection = getConnection();

// Fired when connection is established and session attached
connection.onopen = function(session, details) {
    console.log('Connection to sensor opened');

    function laptimer_changed(details) {
        console.log('TODO: [laptimer_changed]');
    }
    sessionSubscribe(session, 'laptimer_changed', laptimer_changed);

    function sensor_changed(details) {
        console.log('TODO: [sensor_changed]');
    }
    sessionSubscribe(session, 'sensor_changed', sensor_changed);

    function sensor_event(details) {
        console.log('TODO: [sensor_event]');
    }
    sessionSubscribe(session, 'sensor_event', sensor_event);

    function laptimer_options(details) {
        console.log('TODO: Update laptimer options view model...');
    }
    sessionCall(session, 'get_laptimer_options', [], laptimer_options);

    function laptimer_config(details) {
        console.log('TODO: Update laptimer config view model...');
    }
    sessionCall(session, 'get_laptimer_config', [], laptimer_config);

    mainVM.admin.status.laptimer(true);
};

connection.onclose = function(reason, details) {
    mainVM.admin.status.laptimer(false);
    console.log('Connection to laptimer closed (' + reason + ')');
};

connection.open();
