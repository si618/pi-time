// Pi-time knockout scripts and models shared between laptimer and sensor

// Observable that retrieves its value when first bound
// http://www.knockmeout.net/2011/06/lazy-loading-observable-in-knockoutjs.html
ko.onDemandObservable = function(callback, target) {
    var _value = ko.observable(); //private observable

    var result = ko.computed({
        read: function() {
            //if it has not been loaded, execute the supplied function
            if (!result.loaded()) {
                callback.call(target);
            }
            //always return the current value
            return _value();
        },
        write: function(newValue) {
            //indicate that the value is now loaded and set it
            result.loaded(true);
            _value(newValue);
        },
        deferEvaluation: true //do not evaluate immediately when created
    });

    //expose the current state, which can be bound against
    result.loaded = ko.observable();
    //load it again
    result.refresh = function() {
        result.loaded(false);
    };

    return result;
};

function PlayaModel(playa, player, plays) {
    var self = this;
    self.playa = playa; // Where its played, e.g. track
    self.player = player; // Whose playing, e.g. rider
    self.plays = plays; // What is played,
}

function UnitOfMeasurementModel(unitOfMeasurement, description) {
    var self = this;
    self.unitOfMeasurement = unitOfMeasurement;
    self.description = description;
}

function HardwareModel(hardware, description, layout) {
    var self = this;
    self.hardware = hardware;
    self.description = description;
    self.layout = [];
    for (index = 0; index < layout.length; index++) {
        lay = layout[index];
        layoutModel = new LayoutModel(lay[0], lay[1]);
        self.layout.push(layoutModel);
    }
}

function LayoutModel(pin, description) {
    var self = this;
    self.pin = pin;
    self.description = description;
}

function LocationModel(location, description) {
    var self = this;
    self.location = location;
    self.description = description;
}

