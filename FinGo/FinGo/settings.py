<<<<<<< HEAD


=======
>>>>>>> 8968c86cc64b58ba616da23ce3a1e381a382f258
import os
from pathlib import Path

# BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'django-insecure-^1^tr2h2_oe@v005h*2*x8&!o!60k7rtb7rpbq(!mv-l=f)@ur'
<<<<<<< HEAD
=======

>>>>>>> 8968c86cc64b58ba616da23ce3a1e381a382f258
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'e-commerce-django-xbxh.onrender.com']


<<<<<<< HEAD
=======


>>>>>>> 8968c86cc64b58ba616da23ce3a1e381a382f258
# 0ec5238884d3a3d57e46751560b34b58 SECRET_KEY
# MEDIA & STATIC
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
<<<<<<< HEAD
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
=======

STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  
# Use WhiteNoise to serve static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
>>>>>>> 8968c86cc64b58ba616da23ce3a1e381a382f258

# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp.apps.MyappConfig',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
<<<<<<< HEAD
    'django.contrib.sessions.middleware.SessionMiddleware',  # important
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # important
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
=======
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
>>>>>>> 8968c86cc64b58ba616da23ce3a1e381a382f258
]

ROOT_URLCONF = 'FinGo.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
<<<<<<< HEAD
=======
                'django.template.context_processors.media',  # optional if you use MEDIA_URL in templates
>>>>>>> 8968c86cc64b58ba616da23ce3a1e381a382f258
            ],
        },
    },
]

WSGI_APPLICATION = 'FinGo.wsgi.application'

<<<<<<< HEAD
# DATABASE (MySQL)
=======
>>>>>>> 8968c86cc64b58ba616da23ce3a1e381a382f258

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fingo_db',
        'USER': 'fingo_db_user',
        'PASSWORD': '9ibjLUHm8DKPz4AlkhpiwenkhLkjUFFE',
        'HOST': 'dpg-d4fu0t2dbo4c739r0e8g-a.singapore-postgres.render.com',
        'PORT': '5432',
           'OPTIONS': {
            'sslmode': 'require'  # <- THIS LINE IS CRUCIAL
        }
    }
}

<<<<<<< HEAD
=======

>>>>>>> 8968c86cc64b58ba616da23ce3a1e381a382f258
# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# DEFAULT PK
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN/LOGOUT
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/login/'

# SESSION CONFIGURATION (persistent sessions)
<<<<<<< HEAD
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # store sessions in DB
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Sessions persist after browser close
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = True  # Changed to True for better session persistence
CSRF_COOKIE_SECURE = False  # Add this for development
=======
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = False  # True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_SECURE = False  # True in production with HTTPS
>>>>>>> 8968c86cc64b58ba616da23ce3a1e381a382f258
