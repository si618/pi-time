function StatusViewModel() {
    var self = this;

    self.sensorLabel = ko.observable('Connected to sensor');
    self.triggerLabel = ko.observable('Connected to sensor trigger');
    self.triggeredLabel = ko.observable('Sensor triggered');
    self.laptimerLabel = ko.observable('Connected to laptimer');
    self.heartbeatLabel = ko.observable('Laptimer heartbeat');
    self.lapLabel = ko.observable('Active lap');

    self.sensor = ko.observable(false);
    self.trigger = ko.observable(false);
    self.triggered = ko.observable(false);
    self.laptimer = ko.observable(false);
    self.heartbeat = ko.observable(false);
    self.lap = ko.observable(false);
}

function EventsViewModel() {
    var self = this;
    self.events = ko.observable();
}

function SettingsViewModel() {
    // Data
    var self = this;

    // Behaviours
}

function LogsViewModel() {
    // Data
    var self = this;

    // Behaviours
}

function AccessViewModel() {
    var self = this;
    self.authenticated = ko.observable(false);
    self.role = ko.observable('anonymous');
    self.accessLabel = ko.pureComputed(function() {
        return self.authenticated() ? 'Logout' : 'Login';
    }, this);
}

function SensorViewModel() {
    var self = this;

    // Nested view models
    self.status = new StatusViewModel();
    self.events = new EventsViewModel();
    self.settings = new SettingsViewModel();
    self.logs = new LogsViewModel();
    self.access = new AccessViewModel();

    // Data
    self.tabs = ['Status', 'Events', 'Settings', 'Log', 'Access'];
    self.selectedTabId = ko.observable();
    self.selectedTabData = ko.observable();

    // TODO: Tab should be disabled if sensor connection lost or not authorised.
    // Status tab always enabled for all users.
    // Settings and Log tab only enabled if authorised.
    // Events, Settings and Access tabs only enabled if sensor connected.

    // Behaviours
    self.goToTab = function(tab) {
        location.hash = tab;
    };
    self.getTabName = function(tab) {
        if (tab == 'Access') {
            return self.access.accessLabel();
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

sensorVM = new SensorViewModel();
ko.applyBindings(sensorVM);
