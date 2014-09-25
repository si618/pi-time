// Knockout specific code for laptimer web app

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
    self.sensors = ko.observableArray();
    self.lap = ko.observable(false);

    self.laptimerLabel  = ko.observable('Connected to laptimer');
    self.sensorLabel    = ko.observableArray();
    self.triggeredLabel = ko.observableArray();
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

    // Autobahn websocket connections
    var connection = null;
    var sensorConnections = []; // One connection per sensor

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

vm = new MainViewModel();
ko.applyBindings(vm);
