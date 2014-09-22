function StatusViewModel() {
    var self = this;

    self.sensor = ko.observable(false);
    self.laptimer = ko.observable(false);
    self.heartbeat = ko.observable(false);
    self.triggered = ko.observable(false);
    self.lap = ko.observable(false);

    self.sensorLabel = ko.observable('Connected to sensor');
    self.laptimerLabel = ko.observable('Connected to laptimer');
    self.heartbeatLabel = ko.observable('Laptimer heartbeat');
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


    // Behaviours
}

function AccessViewModel() {
    var self = this;
    self.authenticated = ko.observable(false);
    self.role = ko.observable('anonymous');
    self.label = ko.pureComputed(function() {
        return self.authenticated() ? 'Logout' : 'Login';
    }, this);

    // Behaviours
}

function MainViewModel() {
    var self = this;

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
        return tab;
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

mainVM = new MainViewModel();
ko.applyBindings(mainVM);
