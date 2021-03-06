# Django settings for easy project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('bchruszc', 'my_email@domain.com')
    # ('Your Name', 'your_email@domain.com'),
)  

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'bchruszc_nascar'             # Or path to database file if using sqlite3.
DATABASE_USER = 'bchruszc_nascar'             # Not used with sqlite3.
DATABASE_PASSWORD = 'fobelrules'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/bchruszc/webapps/nascar_2008/myproject/media'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/nascar2008_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'
#ADMIN_MEDIA_PREFIX = '/home/brad/html/easy_media/'
#ADMIN_MEDIA_PREFIX = '/media'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'q8uj!1+nc5j=xmzl4d67aub&7$bqr%e!p+on3(#x-r4c3v9#em'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'system.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/bchruszc/webapps/nascar_2008/myproject/templates/',
)

#CACHE_BACKEND = "db://pool_cache"

INSTALLED_APPS = (
#    'django.contrib.auth',
    'django.contrib.contenttypes',
#    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
#    'easy.account',
    'system.pool',
)
