// Pi-time knockout scripts shared between laptimer and sensor

// Observable that retrieves its value when first bound
// http://www.knockmeout.net/2011/06/lazy-loading-observable-in-knockoutjs.html
ko.onDemandObservable = function (callback, target) {
    var _value = ko.observable(); //private observable

    var result = ko.computed({
        read: function () {
            //if it has not been loaded, execute the supplied function
            if (!result.loaded()) {
                callback.call(target);
            }
            //always return the current value
            return _value();
        },
        write: function (newValue) {
            //indicate that the value is now loaded and set it
            result.loaded(true);
            _value(newValue);
        },
        deferEvaluation: true //do not evaluate immediately when created
    });

    //expose the current state, which can be bound against
    result.loaded = ko.observable();
    //load it again
    result.refresh = function () {
        result.loaded(false);
    };

    return result;
};

// Fix for bootstrap-select issue with knockout http://stackoverflow.com/a/22001770/44540
ko.bindingHandlers.selectPicker = {
    init: function (element, valueAccessor, allBindingsAccessor) {
        var $element = $(element);
        $element.addClass("selectpicker").selectpicker();

        var doRefresh = function () {
            $element.selectpicker("refresh");
        }, subscriptions = [];

        // KO 3 requires subscriptions instead of relying on this binding"s update
        // function firing when any other binding on the element is updated.

        // Add them to a subscription array so we can remove them when KO
        // tears down the element.  Otherwise you will have a resource leak.
        var addSubscription = function (bindingKey) {
            var targetObs = allBindingsAccessor.get(bindingKey);

            if (targetObs && ko.isObservable(targetObs)) {
                subscriptions.push(targetObs.subscribe(doRefresh));
            }
        };

        addSubscription("options");
        addSubscription("value");           // Single
        addSubscription("selectedOptions"); // Multiple

        ko.utils.domNodeDisposal.addDisposeCallback(element, function () {
            while (subscriptions.length) {
                subscriptions.pop().dispose();
            }
        });
    },
    update: function (element, valueAccessor, allBindingsAccessor) {
    }
};