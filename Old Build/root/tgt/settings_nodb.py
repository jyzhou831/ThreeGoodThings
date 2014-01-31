# Django settings for tgt project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
        # ('Your Name', 'your_email@domain.com'),
    )

EMAIL_HOST = ''  ### fill this in
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = ''  ### fill this in
EMAIL_HOST_USER = 'reminders@threegthings.net'
EMAIL_SUBJECT_PREFIX = '[3GT]'
EMAIL_USE_TLS = True

MANAGERS = ADMINS
ANONYMOUS_USER_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'threegoodthings',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            }
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Detroit'
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/static/"
STATICFILES_ROOT = '/home/logicalrealist/threegthings.net/public/media/'
STATIC_ROOT = '/home/logicalrealist/threegthings.net/public/static/'

# URL that handles the static files served from STATICFILES_ROOT.
# Example: "http://static.lawrence.com/", "http://example.com/static/"
STATICFILES_URL = 'http://www.threegthings.net/static/'

# URL prefix for admin media -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

# A list of locations of additional static files
STATICFILES_DIRS = ('/home/logicalrealist/threegthings.net/public/media/',)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
        )

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/logicalrealist/threegthings.net/public/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7vwp0+x09vx6keu*y&l5hk^jb1jet2sv6aqnz$7-r$oap!&5ac'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
         'django.middleware.gzip.GZipMiddleware',
    )

ROOT_URLCONF = 'tgt.urls'

TEMPLATE_DIRS = (
        '/home/logicalrealist/threegthings.net/tgt/templates',
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )

INSTALLED_APPS = (

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'registration', The default is now not to use django registration
    'django_facebook',
    'member',
    'south',
    'tgt',
    'django.contrib.admin',
    'userena',
    'guardian',
    )


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#REGISTRATION_BACKEND = 'registration.backends.default.DefaultBackend'
FACEBOOK_REGISTRATION_BACKEND = 'django_facebook.registration_backends.UserenaBackend'
FACEBOOK_APP_ID = ''
FACEBOOK_APP_SECRET = ''
FACEBOOK_STORE_LIKES = False
FACEBOOK_STORE_FRIENDS = False
FACEBOOK_LOGIN_DEFAULT_REDIRECT = '/facebook/connect/'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

FACEBOOK_REGISTRATION_FORM = 'userena.forms.SignupForm'
FACEBOOK_REGISTRATION_TEMPLATE = 'userena/signup_form.html'

AUTHENTICATION_BACKENDS = (
    'django_facebook.auth_backends.FacebookBackend',
    'userena.backends.UserenaAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'member.UserProfile'
STATIC_URL = '/static/'
ACCOUNT_ACTIVATION_DAYS = 10
TEMPLATE_CONTEXT_PROCESSORS = (
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.debug',
            'django.core.context_processors.i18n',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            'django.core.context_processors.request',
            'django.contrib.messages.context_processors.messages',
            'django_facebook.context_processors.facebook',
        )
