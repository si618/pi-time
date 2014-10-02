// Knockout specific code for sensor web app

function StatusViewModel() {
    var self = this;

    self.laptimer = ko.observable(false); /* TODO: Needs to link to event on sensor app on server */
    self.sensor = ko.observable(false);
    self.triggered = ko.observable(false);
    self.lap = ko.observable(false);

    self.laptimerLabel = ko.observable('Connected to laptimer');
    self.sensorLabel = ko.observable('Connected to sensor');
    self.triggeredLabel = ko.observable('Sensor triggered');
    self.lapLabel = ko.observable('Active lap');
}

function LaptimerViewModel() {
    var self = this;

    self.nameLabel = ko.observable('Name');
    self.urlLabel = ko.observable('Address');

    self.laptimerName = ko.observable();
    self.laptimerUrl = ko.observable();

    // Behaviours
    self.updateConfig = function(laptimer) {
        self.laptimerName(laptimer.name);
        self.laptimerUrl(laptimer.url);
    };
}

function SensorViewModel() {
    var self = this;

    self.nameLabel = ko.observable('Name');
    self.urlLabel = ko.observable('Address');
    self.hardwareLabel = ko.observable('Hardware');
    self.locationLabel = ko.observable('Location');

    self.sensorName = ko.observable();
    self.sensorUrl = ko.observable();
    self.hardware = ko.observable();
    self.location = ko.observable();

    // Behaviours
    self.updateConfig = function(sensor) {
        self.sensorName(sensor.name);
        self.sensorUrl(sensor.url);
        self.hardware(sensor.hardware);
        self.location(sensor.location);
    };
}

function EventsViewModel() {
    var self = this;
    self.events = ko.observable();
}

function LogsViewModel() {
    var self = this;
    self.logs = ko.observable();
}

function AccessViewModel() {
    var self = this;

    self.authenticated = ko.observable(false);
    self.role = ko.observable('anonymous');

    // UI
    self.accessLabel = ko.pureComputed(function() {
        return self.authenticated() ? 'Logout' : 'Login';
    }, this);
    self.secretLabel = ko.observable('Password');
    self.secret = ko.observable();
    self.accessingLabel = ko.pureComputed(function() {
        return self.authenticated() ? 'Logging out...' : 'Logging in...';
    }, this);

    // Behaviours
    function authenticated(result) {
        console.log('authenticated: ' + result);
    }
    self.authenticate = function(tab) {
        rpc('authenticate', authenticated, {
            'params': [self.secret]
        });
    };
}

function MainViewModel() {
    var self = this;

    // Autobahn websocket connections
    var connection = null;
    var laptimerConnection = null;

    // Nested view models
    self.status = new StatusViewModel();
    self.laptimer = new LaptimerViewModel();
    self.sensor = new SensorViewModel();
    self.events = new EventsViewModel();
    self.logs = new LogsViewModel();
    self.access = new AccessViewModel();

    // Menu
    self.menuLabel = ko.observable('Menu');
    self.fullscreenLabel = ko.observable('Fullscreen');
    self.selectedMenu = ko.observable('Status');
    self.statusLabel = ko.observable('Status');
    self.settingsLabel = ko.observable('Settings');
    self.laptimerLabel = ko.observable('Laptimer');
    self.sensorLabel = ko.observable('Sensor');
    self.eventsLabel = ko.observable('Sensor Events');
    self.logsLabel = ko.observable('Console Log');
    self.accessLabel = ko.pureComputed(function() {
        return self.access.accessLabel();
    }, this);
    self.appTitle = ko.pureComputed(function() {
        if (self.laptimer.laptimerName() === undefined || self.sensor.sensorName() === undefined) {
            return '';
        }
        return self.laptimer.laptimerName() + ' - ' + self.sensor.sensorName();
    }, this);

    // TODO: Tab should be disabled if sensor connection lost or not authorised.
    // Status tab always enabled for all users.
    // Settings tab only enabled if authorised.
    // Settings and Access tabs only enabled if sensor connected.

    // Behaviours
    self.selectMenu = function(menu) {
        location.hash = menu;
    };

    // Client-side routes
    Sammy(function() {
        this.get('#:menu', function() {
            self.selectedMenu(this.params.menu);
        });
    }).run();
}

vm = new MainViewModel();
ko.applyBindings(vm);
