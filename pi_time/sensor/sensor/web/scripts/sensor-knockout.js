// Knockout specific code for sensor web app

function StatusViewModel() {
    var self = this;

    self.laptimer = ko.observable(false);
    self.sensor = ko.observable(false);
    self.triggered = ko.observable(false);
    self.lap = ko.observable(false);

    self.laptimerLabel = ko.observable('Connected to laptimer');
    self.sensorLabel = ko.observable('Connected to sensor');
    self.triggeredLabel = ko.observable('Sensor triggered');
    self.lapLabel = ko.observable('Active lap');
}

function EventsViewModel() {
    var self = this;
    self.events = ko.observable();
}

function SettingsViewModel() {
    var self = this;

    self.nameLabel = ko.observable('Name');
    self.urlLabel = ko.observable('Address');
    self.hardwareLabel = ko.observable('Hardware');
    self.locationLabel = ko.observable('Location');

    self.laptimerName = ko.observable();
    self.laptimerUrl = ko.observable();
    self.sensorName = ko.observable();
    self.sensorUrl = ko.observable();
    self.hardware = ko.observable();
    self.location = ko.observable();

    // Tab data
    self.tabs = ['Settings-Laptimer', 'Settings-Sensor'];
    self.selectedTabId = ko.observable();
    self.selectedTabData = ko.observable();

    // Behaviours
    function todo(result) {
        console.log('todo: ' + result);
        sensor = details[0];
        self.sensorName(sensor.name);
        self.sensorUrl(sensor.url);
        self.hardware(sensor.hardware);
        self.location(sensor.location);
    }
    self.temp = function() {
        rpc('get_sensor_config', todo);
    };
}

function AccessViewModel() {
    var self = this;

    self.authenticated = ko.observable(false);
    self.role = ko.observable('anonymous');

    // UI
    self.secretLabel = ko.observable('Password');
    self.secret = ko.observable();

    // Tab label
    self.label = ko.pureComputed(function() {
        return self.authenticated() ? 'Logout' : 'Login';
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
    self.events = new EventsViewModel();
    self.settings = new SettingsViewModel();
    self.access = new AccessViewModel();

    // Tab data
    self.tabs = ['Status', 'Events', 'Settings', 'Access'];
    self.selectedTabId = ko.observable();
    self.selectedTabData = ko.observable();

    // TODO: Tab should be disabled if sensor connection lost or not authorised.
    // Status tab always enabled for all users.
    // Settings tab only enabled if authorised.
    // Settings and Access tabs only enabled if sensor connected.

    // Behaviours
    self.goToTab = function(tab) {
        location.hash = tab;
    };
    self.getTabName = function(tab) {
        if (tab == 'Access') {
            return self.access.label();
        }
        return tab.substring(tab.lastIndexOf('-') + 1);
    };

    // Client-side routes
    Sammy(function() {
        this.get('#:tab', function() {
            self.selectedTabId(this.params.tab);
        });

        this.get('', function() {
            this.app.runRoute('get', '#Status');
        });
    }).run();
}

vm = new MainViewModel();
ko.applyBindings(vm);
