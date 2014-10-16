module.exports = function (grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        nose: {
            options: {
                rednose: false
            },
            pi_time: {
                src: 'pi_time'
            }
        },
        pylint: {
            pi_time: {
                src: ['pi_time/pi_time']
            },
            laptimer: {
                src: ['pi_time/laptimer']
            },
            sensor: {
                src: ['pi_time/sensor']
            }
        },
        jshint: {
            options: {
                curly: true
            },
            pi_time: {
                src: ['pi_time/pi_time/web/js/pi-time*.js']
            },
            laptimer: {
                src: ['pi_time/laptimer/laptimer/web/js/laptimer*.js']
            },
            sensor: {
                src: ['pi_time/sensor/sensor/web/js/sensor*.js']
            }
        },
        bootlint: {
            options: {
                stoponerror: false,
                relaxerror: []
            },
            files: ['pi_time/pi_time/web/*.html']
        },
        clean: ['dist'],
        copy: {
            options: {
                dot: true
            },
            laptimer: {
                files: [
                    {
                        src: ['pi_time/pi_time/**/*.py', 'pi_time/laptimer/**/*.py', 'pi_time/laptimer/.crossbar/*', 'pi_time/laptimer/**/*.json', 'pi_time/laptimer/**/*.html', '!pi_time/pi_time/**/test/**', '!pi_time/laptimer/**/test/**'],
                        dest: 'dist/laptimer',
                        expand: true
                    }
                ]
            },
            sensor: {
                files: [
                    {
                        src: ['pi_time/pi_time/**/*.py', 'pi_time/sensor/**/*.py', 'pi_time/sensor/.crossbar/*', 'pi_time/sensor/**/*.json', 'pi_time/sensor/**/*.html', '!pi_time/pi_time/**/test/**', '!pi_time/sensor/**/test/**'],
                        dest: 'dist/sensor',
                        expand: true
                    }
                ]
            },
            laptimer_web_fonts: {
                files: [
                    {
                        cwd: 'pi_time/pi_time/',
                        src: ['web/fonts/*.svg'],
                        dest: 'dist/laptimer/pi_time/laptimer/laptimer/',
                        expand: true
                    }
                ]
            },
            sensor_web_fonts: {
                files: [
                    {
                        cwd: 'pi_time/pi_time/',
                        src: ['web/fonts/*.svg'],
                        dest: 'dist/sensor/pi_time/sensor/sensor/',
                        expand: true
                    }
                ]
            }
        },
        concat: {
            options: {
                separator: ';'
            },
            pi_time_laptimer_js: {
                src: ['pi_time/pi_time/web/js/jquery*.js', 'pi_time/pi_time/web/js/*.js'],
                dest: 'dist/laptimer/pi_time/laptimer/laptimer/web/js/libs.js'
            },
            pi_time_sensor_js: {
                src: ['pi_time/pi_time/web/js/jquery*.js', 'pi_time/pi_time/web/js/*.js'],
                dest: 'dist/sensor/pi_time/sensor/sensor/web/js/libs.js'
            },
            laptimer_js: {
                src: ['pi_time/laptimer/laptimer/web/js/laptimer*.js'],
                dest: 'dist/laptimer/pi_time/laptimer/laptimer/web/js/libs-laptimer.js'
            },
            sensor_js: {
                src: ['pi_time/sensor/sensor/web/js/sensor*.js'],
                dest: 'dist/sensor/pi_time/sensor/sensor/web/js/libs-sensor.js'
            },
            laptimer_css: {
                src: ['pi_time/pi_time/web/css/*.css', 'laptimer/laptimer/web/css/*.css'],
                dest: 'dist/laptimer/pi_time/laptimer/laptimer/web/css/pi-time-laptimer.css'
            },
            sensor_css: {
                src: ['pi_time/pi_time/web/css/*.css', 'sensor/sensor/web/css/*.css'],
                dest: 'dist/sensor/pi_time/sensor/sensor/web/css/pi-time-sensor.css'
            }
        },
        htmlmin: {
            laptimer: {
                options: {
                    removeComments: true,
                    collapseWhitespace: true
                },
                files: {
                    'dist/laptimer/pi_time/laptimer/laptimer/web/index.html': 'dist/laptimer/pi_time/laptimer/laptimer/web/index.html'
                }
            },
            sensor: {
                options: {
                    removeComments: true,
                    collapseWhitespace: true
                },
                files: {
                    'dist/sensor/pi_time/sensor/sensor/web/index.html': 'dist/sensor/pi_time/sensor/sensor/web/index.html'
                }
            }
        },
        uglify: {
            options: {
                compress: true,
                mangle: true,
                preserveComments: false,
                sourceMap: true
            },
            laptimer: {
                files: {
                    'dist/laptimer/pi_time/laptimer/laptimer/web/js/libs.js': 'dist/laptimer/pi_time/laptimer/laptimer/web/js/libs.js',
                    'dist/laptimer/pi_time/laptimer/laptimer/web/js/libs-laptimer.js': 'dist/laptimer/pi_time/laptimer/laptimer/web/js/libs-laptimer.js'
                }
            },
            sensor: {
                files: {
                    'dist/sensor/pi_time/sensor/sensor/web/js/libs.js': 'dist/sensor/pi_time/sensor/sensor/web/js/libs.js',
                    'dist/sensor/pi_time/sensor/sensor/web/js/libs-sensor.js': 'dist/sensor/pi_time/sensor/sensor/web/js/libs-sensor.js'
                }
            }
        },
        cssmin: {
            options: {
                keepSpecialComments: 0
            },
            laptimer: {
                files: {
                    'dist/laptimer/pi_time/laptimer/laptimer/web/css/pi-time-laptimer.css': 'dist/laptimer/pi_time/laptimer/laptimer/web/css/pi-time-laptimer.css'
                }
            },
            sensor: {
                files: {
                    'dist/sensor/pi_time/sensor/sensor/web/css/pi-time-sensor.css': 'dist/sensor/pi_time/sensor/sensor/web/css/pi-time-sensor.css'
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-bootlint');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-htmlmin');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-nose');
    grunt.loadNpmTasks('grunt-pylint');

    grunt.registerTask('default', ['nose', 'jshint', 'bootlint', 'clean', 'copy', 'concat']);
    grunt.registerTask('dist', ['clean', 'copy', 'concat']);
    grunt.registerTask('lint', ['pylint', 'jshint', 'bootlint']);
    grunt.registerTask('minify', ['dist', 'htmlmin', 'uglify', 'cssmin']);
    grunt.registerTask('test', ['nose']);
    grunt.registerTask('release', ['lint', 'test', 'minify']);

};
