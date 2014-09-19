function SessionViewModel() {
    // Data
    var self = this;

    // Behaviours
}

function TrackRecordsViewModel() {
    // Data
    var self = this;

    // Behaviours
}

function PlayaRecordsViewModel() {
    // Data
    var self = this;

    // Behaviours
}

function SessionRecordsViewModel() {
    // Data
    var self = this;

    // Behaviours
}

function RecordsViewModel() {
    // Data
    var self = this;

    // Behaviours
}

function StatusViewModel() {
    var self = this;

    self.laptimer = ko.observable(false);
    //self.sensor = ko.observable(false); TODO: Array of sensors
    self.lap = ko.observable(false);

    self.laptimerLabel  = ko.observable('Connected to laptimer');
    //self.sensorLabel    = ko.observable('Connected to sensor'); TODO: Array of sensors
    //self.triggeredLabel = ko.observable('Sensor triggered'); TODO: Array of sensors
    self.lapLabel = ko.observable('Active lap');
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

function AdminViewModel() {
    // Data
    var self = this;

    self.status = new StatusViewModel();
    self.events = new EventsViewModel();
    self.settings = new SettingsViewModel();

    // Behaviours
}

function AccessViewModel() {
    var self = this;
    self.authenticated = ko.observable(false);
    self.role = ko.observable('anonymous');
    self.label = ko.pureComputed(function() {
        return self.authenticated() ? 'Logout' : 'Login';
    }, this);
}

function MainViewModel() {
    var self = this;

    // Nested view models
    self.session = new SessionViewModel();
    self.records = new RecordsViewModel();
    self.admin = new AdminViewModel();
    self.access = new AccessViewModel();

    // Tab data
    self.tabs = ['Session', 'Records', 'Admin', 'Access'];
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
            this.app.runRoute('get', '#Session');
        });
    }).run();
}

mainVM = new MainViewModel();
ko.applyBindings(mainVM);
