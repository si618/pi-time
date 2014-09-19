// Pi-time general scripts shared between laptimer and sensor apps

// Subvert console log to output to div in window as well as console
if (typeof console != 'undefined') {
    if (typeof console.log != 'undefined') {
        console._log = console.log;
    } else {
        console._log = function() {};
    }
}
console.log = function(message) {
    // Always uppercase first character for consistency
    message = message.charAt(0).toUpperCase() + message.slice(1);
    console._log(message);
    log = $('#log');
    log.text(log.text() + '[' + getLocalTime() + '] ' + message + '\n');
    log.scrollTop(log[0].scrollHeight);
};
console.error = console.debug = console.info = console.log;


// Helper function to get formatted current local time including milliseconds
function getLocalTime() {
    now = new Date();
    hours = now.getHours();
    if (hours < 10) {
        hours = '0' + hours;
    }
    minutes = now.getMinutes();
    if (minutes < 10) {
        minutes = '0' + minutes;
    }
    seconds = now.getSeconds();
    if (seconds < 10) {
        seconds = '0' + seconds;
    }
    milliseconds = now.getMilliseconds();
    if (milliseconds < 10) {
        milliseconds = '00' + milliseconds;
    } else if (milliseconds < 100) {
        milliseconds = '0' + milliseconds;
    }
    time = hours + ':' + minutes + ':' + seconds + ':' + milliseconds;
    return time;
}


// Helper function to parse JSON, default to native parser, jquery as fallback
function parseJson(json) {
    return JSON && JSON.parse(json) || $.parseJSON(json);
}

function printError(error) {
    msg = error.error;
    if (error.args.length > 0) {
        msg += ': ' + error.args[0];
    }
    return msg;
}

// Activate full screen mode for different browsers
function goFullscreen() {
    element = document.documentElement;
    if (element.requestFullscreen) {
        element.requestFullscreen();
    } else if (element.mozRequestFullScreen) {
        element.mozRequestFullScreen();
    } else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullscreen();
    } else if (element.msRequestFullscreen) {
        element.msRequestFullscreen();
    }
}
// Toggles full screen state
function fullscreenChanged() {
    $('.fullscreen').toggle();
}
// Wire up full screen events in different browsers
document.addEventListener('fullscreenchange', fullscreenChanged);
document.addEventListener('webkitfullscreenchange', fullscreenChanged);
document.addEventListener('mozfullscreenchange', fullscreenChanged);
document.addEventListener('MSFullscreenChange', fullscreenChanged);

// Monitor resize events to resize matching 'output' class element
$(document).ready(function() {
    function resizeOutput() {
        var height = $(window).height() - 100;
        output = $('.output');
        output.height(height);
        output.scrollTop = output.height;
    }
    resizeOutput();
    $(window).resize(function() {
        resizeOutput();
    });
});
