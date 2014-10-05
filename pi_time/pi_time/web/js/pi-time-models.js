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

