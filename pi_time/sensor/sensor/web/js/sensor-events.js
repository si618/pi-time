// Autobahn events updating knockout view models

function connectionOpened(details) {
    console.log('Connection to sensor opened (' + wsuri + ' - session ' + session.id + ')');
    rpc('get_laptimer_config', laptimerConfig); // TODO: Lazy load in laptimer view model
    rpc('get_sensor_config', sensorConfig); // TODO: Lazy load in sensor view model
    rpc('get_sensor_options', sensorOptions); // TODO: Lazy load on sensor view model
    vm.status.sensor(true);
}

function connectionClosed(reason, details) {
    console.log('Connection to sensor closed (' + reason + ')');
    vm.status.sensor(false);
}

function sensorChanged(details) {
    console.log('[sensor_changed]');
    // ko.mapping.fromJS(details[0], vm.sensor); TODO: Not working?
    sensorConfig(details);
}

function sensorTriggered(details) {
    console.log('Event sensor_triggered (' + details + ')');
    // ko.mapping.fromJS(details, vm.status);
    vm.status.triggered(true);
    setTimeout(function () {
        vm.status.triggered(false);
    }, 1000);
}

function sensorConfig(details) {
    // ko.mapping.fromJSON(details[0], vm.sensor); TODO: Not working?
    var sensor = details[0];
    vm.sensor.name(sensor.name);
    vm.sensor.url(sensor.url);
    vm.sensor.hardware(sensor.hardware);
    vm.sensor.location(sensor.location);
}

function sensorOptions(details) {
    // ko.mapping.fromJSON(options, vm.sensor); TODO: Not working?
    vm.sensor.hardwares.removeAll();
    var hw, hwModel;
    for (var index = 0; index < details.hardwares.length; index++) {
        hw = details.hardwares[index];
        hwModel = new HardwareModel(hw[0], hw[1], hw[2]);
        vm.sensor.hardwares.push(hwModel);
    }
    vm.sensor.locations.removeAll();
    var loc, locModel;
    for (index = 0; index < details.locations.length; index++) {
        loc = details.locations[index];
        locModel = new LocationModel(loc[0], loc[1]);
        vm.sensor.locations.push(locModel);
    }
}

function laptimerConfig(laptimer) {
    // ko.mapping.fromJS(details, vm.laptimer); TODO: Not working?
    vm.laptimer.name(laptimer.name);
    vm.laptimer.url(laptimer.url);
}

function laptimerStarted(details) {
    console.log('[laptimer_started]' + details);
    vm.status.laptimer(true);
}

function laptimerStopped(details) {
    console.log('[laptimer_stopped]' + details);
    vm.status.laptimer(false);
}

function laptimerChanged(laptimer) {
    console.log('[laptimer_changed]');
    // ko.mapping.fromJS(laptimer, vm.laptimer); TODO: Not working?
    laptimerConfig(laptimer);
}

function lapStarted(details) {
    console.log('[lap_started] ' + details);
    vm.status.lap(true);
}

function lapFinished(details) {
    console.log('[lap_finished]' + details);
    vm.status.lap(false);
}

function lapCancelled(details) {
    console.log('[lap_cancelled]' + details);
    vm.status.lap(false);
}
