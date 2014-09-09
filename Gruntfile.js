module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        concat: {
            options: {
                separator: ';'
            },
            laptimer: {
                src: ['pi_time/pi_time/web/scripts/jquery*.js', 'pi_time/pi_time/web/scripts/autobahn*.js', 'pi_time/pi_time/web/scripts/knockout*.js', 'pi_time/pi_time/web/scripts/sammy*.js', 'pi_time/pi_time/web/scripts/pi-time-common.js'],
                dest: 'pi_time/laptimer/laptimer/web/scripts/lib.js'
            },
            sensor: {
                src: ['pi_time/pi_time/web/scripts/jquery*.js', 'pi_time/pi_time/web/scripts/autobahn*.js', 'pi_time/pi_time/web/scripts/knockout*.js', 'pi_time/pi_time/web/scripts/sammy*.js', 'pi_time/pi_time/web/scripts/pi-time-common.js'],
                dest: 'pi_time/sensor/sensor/web/scripts/lib.js'
            },
        },
    });

    grunt.loadNpmTasks('grunt-contrib-concat');

    grunt.registerTask('default', ['concat']);

};
