function StatusViewModel() {
    // Data
    var self = this;

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

function SensorViewModel() {
    // Data
    var self = this;
    self.tabs = ['Status', 'Events', 'Settings', 'Log', 'Authenticate'];
    self.selectedTabId = ko.observable();
    self.selectedTabData = ko.observable();
    self.status = ko.observable();
    self.settings = ko.observable();
    self.events = ko.observable();

    // Behaviours
    self.goToTab = function(tab) {
        location.hash = tab
    };
    self.getTabName = function(tab) {
        if (tab == 'Authenticate') {
            // TODO: Logout if already logged in, otherwise Login
            return 'Login'
        }
        else {
            return tab
        }
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

ko.applyBindings(new SensorViewModel());
