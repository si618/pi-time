"""
Django settings for pi_time project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')g$+05jjz%m5e=af27riy%ti!b)cfo5q1)va)z2shmb#$6^+a5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

# Add 1.6 test runner to avoid check warning, just have to wait for 1.7
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_settings', # https://github.com/jqb/django-settings
    'laptimer', # https://github.com/si618/pi-time
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pi_time.urls'

WSGI_APPLICATION = 'pi_time.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'pi-time.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Adelaide'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'laptimer': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gpio': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'twisted': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}

# LapTimer settings

METRIC = 'SI' # Report speed in km/h|m/s, distance in metres.
IMPERIAL = 'IM' # Report speed in m/h|y/s, distance in yards.
UNIT_OF_MEASUREMENT = (
    (METRIC, 'Metric'),
    (IMPERIAL, 'Imperial')
)

SENSOR_TYPE_RPI = 'PI'
SENSOR_TYPE = ( # Defines the type of sensor TODO: i18n
    (SENSOR_TYPE_RPI, 'Raspberry Pi'),
)

SENSOR_POS_START = 'ST'
SENSOR_POS_FINISH = 'FI'
SENSOR_POS_START_FINISH = 'SF'
SENSOR_POS_SECTOR = 'SE'
SENSOR_POS = ( # Defines the sensor position on track TODO: i18n
    (SENSOR_POS_START, 'Start'),
    (SENSOR_POS_FINISH, 'Finish'),
    (SENSOR_POS_START_FINISH, 'Start and finish'),
    (SENSOR_POS_SECTOR, 'Sector checkpoint (split times)'),
)

RPI_GPIO_LAYOUT = (
    (3, '3 = GPIO 2'),
    (5, '5 = GPIO 3'),
    (7, '7 = GPIO 4 (GPCLK0)'),
    (8, '8 = GPIO 14 (UART0_TXD)'),
    (10, '10 = GPIO 15 (UART0_RXD)'),
    (11, '11 = GPIO 17'),
    (12, '12 = GPIO 18 (PCMCLK)'),
    (13, '13 = GPIO 27'),
    (15, '14 = GPIO 22'),
    (16, '15 = GPIO 23'),
    (18, '18 = GPIO 24'),
    (19, '19 = GPIO 10 (SPI0_MOSI)'),
    (21, '21 = GPIO 9 (SPI0_MISO '),
    (22, '22 = GPIO 25'),
    (23, '23 = GPIO 11 (SPI0_SCLK)'),
    (24, '24 = GPIO 8 (SPI0_CE0_N)'),
    (26, '26 = GPIO 7 (SPI0_CE1_N)')
)

DJANGO_SETTINGS = {
    'debug_app': ('Boolean', DEBUG),
    'unit_of_measurement': ('UnitOfMeasurement', METRIC),
    'gpio_app': ('GPIOLayout', 15),
    'gpio_lap': ('GPIOLayout', 16),
    'gpio_sensor': ('GPIOLayout', 18)
}
