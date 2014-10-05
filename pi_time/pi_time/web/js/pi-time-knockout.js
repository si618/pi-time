// Pi-time knockout scripts shared between laptimer and sensor

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
