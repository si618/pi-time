module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        nose: {
            options: {
                rednose: false
            },
            pi_time: {
                src: 'pi_time'
            },
        },
        pylint: {
            options: {
                disable: 'missing-docstring'
            },
            pi_time: {
                src: 'pi_time/pi_time'
            },
            laptimer: {
                src: 'pi_time/laptimer'
            },
            sensor: {
                src: 'pi_time/sensor'
            },
        },
        jshint: {
            options: {
                curly: true
            },
            pi_time: {
                src: ['pi_time/pi_time/web/scripts/pi-time-*.js']
            },
            laptimer: {
                src: ['laptimer/laptimer/web/scripts/laptimer-*.js']
            },
            sensor: {
                src: ['sensor/sensor/web/scripts/sensor-*.js']
            },
        },
        clean: ['dist'],
        copy: {
            options: {
                dot: true
            },
            laptimer: {
                files: [{
                    src: ['pi_time/pi_time/**/*.py', 'pi_time/laptimer/**/*.py', 'pi_time/laptimer/.crossbar/*', 'pi_time/laptimer/**/*.json', 'pi_time/laptimer/**/*.html', '!pi_time/pi_time/**/tests/**', '!pi_time/laptimer/**/tests/**'],
                    dest: 'dist/laptimer',
                    expand: true
                }],
            },
            sensor: {
                files: [{
                    src: ['pi_time/pi_time/**/*.py', 'pi_time/sensor/**/*.py', 'pi_time/sensor/.crossbar/*', 'pi_time/sensor/**/*.json', 'pi_time/sensor/**/*.html', '!pi_time/pi_time/**/tests/**', '!pi_time/sensor/**/tests/**'],
                    dest: 'dist/sensor',
                    expand: true
                }],
            },
        },
        concat: {
            options: {
                separator: ';'
            },
            pi_time_laptimer_js: {
                src: ['pi_time/pi_time/web/scripts/jquery*.js', 'pi_time/pi_time/web/scripts/autobahn*.js', 'pi_time/pi_time/web/scripts/knockout*.js', 'pi_time/pi_time/web/scripts/sammy*.js', 'pi_time/pi_time/web/scripts/pi-time-common.js'],
                dest: 'dist/laptimer/pi_time/laptimer/laptimer/web/scripts/lib.js'
            },
            pi_time_sensor_js: {
                src: ['pi_time/pi_time/web/scripts/jquery*.js', 'pi_time/pi_time/web/scripts/autobahn*.js', 'pi_time/pi_time/web/scripts/knockout*.js', 'pi_time/pi_time/web/scripts/sammy*.js', 'pi_time/pi_time/web/scripts/pi-time-common.js'],
                dest: 'dist/sensor/pi_time/sensor/sensor/web/scripts/lib.js'
            },
            laptimer_js: {
                src: ['pi_time/laptimer/laptimer/web/scripts/laptimer-knockout.js', 'pi_time/laptimer/laptimer/web/scripts/laptimer-crossbar.js'],
                dest: 'dist/laptimer/pi_time/laptimer/laptimer/web/scripts/lib-laptimer.js'
            },
            sensor_js: {
                src: ['pi_time/sensor/sensor/web/scripts/sensor-knockout.js', 'pi_time/sensor/sensor/web/scripts/sensor-crossbar.js'],
                dest: 'dist/sensor/pi_time/sensor/sensor/web/scripts/lib-sensor.js'
            },
            laptimer_css: {
                src: ['pi_time/pi_time/web/styles/pi_time.css', 'laptimer/laptimer/web/styles/laptimer.css'],
                dest: 'dist/laptimer/pi_time/laptimer/laptimer/web/styles/pi-time-laptimer.css'
            },
            sensor_css: {
                src: ['pi_time/pi_time/web/styles/pi_time.css', 'sensor/sensor/web/styles/sensor.css'],
                dest: 'dist/sensor/pi_time/sensor/sensor/web/styles/pi-time-sensor.css'
            },
        },
    });

    grunt.loadNpmTasks('grunt-nose');
    grunt.loadNpmTasks('grunt-pylint');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-concat');

    grunt.registerTask('default', ['nose', 'jshint', 'clean', 'copy', 'concat']);
    grunt.registerTask('dist', ['clean', 'copy', 'concat']);
    grunt.registerTask('lint', ['pylint', 'jshint']);
    grunt.registerTask('test', ['nose']);

};
