// Output console logging to document as well as console
if (typeof console  != 'undefined')
	if (typeof console.log != 'undefined')
		console._log = console.log;
else
	console._log = function() {};
console.log = function(message) {
	console._log(message);
	log = $('#log')
	now = '[' + new Date().toISOString() + '] '
	logval = log.val()
	if (logval.length > 0) { now = '\n' + now }
	log.val(logval + now + message);
    log.scrollTop(log[0].scrollHeight);
};
console.error = console.debug = console.info = console.log


// Knockout code

function SensorViewModel() {
    // Data
    var self = this;
    self.tabs = ['Status', 'Events', 'Settings', 'Log'];
    self.selectedTabId = ko.observable();
    self.selectedTabData = ko.observable();
    self.status = ko.observable();
    self.settings = ko.observable();
    self.events = ko.observable();

    // Behaviours
    self.goToTab = function(tab) {
        location.hash = tab
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


// Crossbar code

// URL of WAMP Router (Crossbar.io)
var wsuri;
if (document.location.origin == 'file://') {
    wsuri = 'ws://127.0.0.1:8888/ws';

} else {
    wsuri = (document.location.protocol === 'http:' ? 'ws:' : 'wss:') + '//' +
        document.location.host + '/ws';
}

// WAMP connection to Router
var connection = new autobahn.Connection({
    url: wsuri,
    realm: 'pi-time'
});

// fired when connection is established and session attached
connection.onopen = function(session, details) {

    console.log('Connected to sensor');

    function on_laptimerevent(args) {
        var laptimer = args[0];
        // TODO: laptimer contain details of status change of laptimer
        // server (start/stop/error) or current lap (started/finished)
        console.log('Event: on_laptimerevent received from laptimer ' + laptimer);
    }
    session.subscribe('io.github.si618.pi-time.onlaptimerevent', on_laptimerevent).then(
        function(sub) {
            console.log('Subscribed to topic: onlaptimerevent');
        },
        function(err) {
            console.log('Failed to subscribe to topic: onlaptimerevent', err);
        }
    );

    function on_sensorevent(args) {
        var sensor = args[0];
        var occured = args[1]
        console.log('Event: on_sensorevent received from sensor ' + sensor);
    }
    session.subscribe('io.github.si618.pi-time.onsensorevent', on_sensorevent).then(
        function(sub) {
            console.log('Subscribed to topic: onsensorevent');
        },
        function(err) {
            console.log('Failed to subscribe to topic: onsensorevent', err);
        }
    );

    function getSensorEvents(args) {
        var sensor = args[0];
        var events = args[1];
        console.log('Got sensor events');
    }
    session.register('io.github.si618.pi-time.getSensorEvents', getSensorEvents).then(
        function(reg) {
            console.log('Registered procedure: getSensorEvents');
        },
        function(err) {
            console.log('Failed to register procedure: getSensorEvents', err);
        }
    );

    function getSensorSetup(args) {
        var hardware = args[0];
        var laptimerServer = args[1];
        var sensorPosition = args[2];
        var sendorConfig = args[3]
        console.log('Got sensor setup');
    }
    session.register('io.github.si618.pi-time.getSensorSetup', getSensorSetup).then(
        function(reg) {
            console.log('Registered procedure: getSensorSetup');
        },
        function(err) {
            console.log('Failed to register procedure: getSensorSetup', err);
        }
    );

    function setSensorSetup(setup) {
        session.call('io.github.si618.pi-time.setSensorSetup', [setup]).then(
            function(res) {
                console.log('Result from setSensorSetup:', res);
            },
            function(err) {
                console.log('Error from setSensorSetup: ', err);
            }
        );
    }
};

// fired when connection was lost (or could not be established)
connection.onclose = function(reason, details) {
    console.log('Connection to sensor lost: ' + reason);
}

connection.open();
