// Subvert console log
if (typeof console != 'undefined')
    if (typeof console.log != 'undefined')
        console._log = console.log;
    else
        console._log = function() {};

console.log = function(message) {
    console._log(message);
    log = $('#log')
    log.text(log.text() + '[' + getLocalTime() + '] ' + message + '\n');
    log.scrollTop(log[0].scrollHeight);
};
console.error = console.debug = console.info = console.log

function getLocalTime() {
    now = new Date();
    hours = now.getHours();
    if (hours < 10) hours = '0' + hours;
    minutes = now.getMinutes();
    if (minutes < 10) minutes = '0' + minutes;
    seconds = now.getSeconds();
    if (seconds < 10) seconds = '0' + seconds;
    milliseconds = now.getMilliseconds();
    if (milliseconds < 10) milliseconds = '00' + milliseconds;
    else if (milliseconds < 100) milliseconds = '0' + milliseconds;
    time = hours + ':' + minutes + ':' + seconds + ':' + milliseconds;
    return time;
}

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

function fullscreenChanged() {
    $('.fullscreen').toggle();
}

document.addEventListener('fullscreenchange', fullscreenChanged);
document.addEventListener('webkitfullscreenchange', fullscreenChanged);
document.addEventListener('mozfullscreenchange', fullscreenChanged);
document.addEventListener('MSFullscreenChange', fullscreenChanged);

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
