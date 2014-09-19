// Pi-time crossbar scripts shared between laptimer and sensor

getConnection = function() {
    // URL of WAMP Router (Crossbar.io)
    protocol = document.location.protocol === 'http:' ? 'ws:' : 'wss:';
    wsuri = protocol + '//' + document.location.host + '/ws';
    // WAMP connection to Router
    var connection = new autobahn.Connection({
        url: wsuri,
        realm: 'pi-time'
    });
    return connection;
};
