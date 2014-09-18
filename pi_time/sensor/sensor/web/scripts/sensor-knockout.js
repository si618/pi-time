function StatusViewModel() {
    // Data
    var self = this;
    self.sensor = ko.observable(false)
    self.sensorTrigger = ko.observable(false)
    self.sensorTriggered = ko.observable(false)
    self.laptimer = ko.observable(false)
    self.laptimerHeartbeat = ko.observable(false)
    self.lap = ko.observable(false)

    // Behaviours
};

function EventsViewModel() {
    var self = this;
    self.events = ko.observable();
};

function SettingsViewModel() {
    // Data
    var self = this;

    // Behaviours
};

function LogsViewModel() {
    // Data
    var self = this;

    // Behaviours
};

function AccessViewModel() {
    // Data
    var self = this;
    self.authenticated = ko.observable(false);

    // Behaviours
    self.getTabName = function() {
        return self.authenticated() ? 'Logout' : 'Login';
    }
};

function SensorViewModel() {
    // Data
    var self = this;

    self.tabs = ['Status', 'Events', 'Settings', 'Log', 'Access'];
    self.selectedTabId = ko.observable();
    self.selectedTabData = ko.observable();

    // Nested view models
    self.status = new StatusViewModel();
    self.events = new EventsViewModel();
    self.settings = new SettingsViewModel();
    self.logs = new LogsViewModel();
    self.access = new AccessViewModel();

    // Behaviours
    self.goToTab = function(tab) {
        location.hash = tab;
    };
    self.getTabName = function(tab) {
        if (tab == 'Access') {
            return self.access.getTabName();
        }
        return tab;
    };

    // Client-side routes
    Sammy(function() {
        this.get('#:tab', function() {
            self.selectedTabId(this.params.tab);
        });

        this.get('', function() {
            this.app.runRoute('get', '#Status')
        });
    }).run();
};

sensorVM = new SensorViewModel();
ko.applyBindings(sensorVM);
