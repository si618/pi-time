// Pi-time models shared between laptimer and sensor

function PlayaModel(playa, player, playing) {
    var self = this;
    self.playa = playa; // Where (pump track)
    self.player = player; // Who (rider)
    self.playing = playing; // What (bike)
}

function UnitOfMeasurementModel(unitOfMeasurement, description) {
    var self = this;
    self.unitOfMeasurement = unitOfMeasurement;
    self.description = description;
}

function HardwareModel(hardware, description, pinout) {
    var self = this;
    self.hardware = hardware;
    self.description = description;
    self.pinout = [];
    for (var index = 0; index < pinout.length; index++) {
        var pin = pinout[index];
        var pinoutModel = new PinoutModel(pin[0], pin[1]);
        self.pinout.push(pinoutModel);
    }
}

function PinoutModel(pin, description) {
    var self = this;
    self.pin = pin;
    self.description = description;
}

function LocationModel(location, description) {
    var self = this;
    self.location = location;
    self.description = description;
}
