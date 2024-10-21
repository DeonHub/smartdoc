import os

from pathlib import Path
import environ


env = environ.Env()
environ.Env.read_env()


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')

STATIC_DIR=os.path.join(BASE_DIR,'static')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dhup^y*ngb9w+-8h2=w^s+ucy0-p7_8f_3c!7tn!jy2xlmyh8_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'callbot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'healthcare.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'healthcare.wsgi.application'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 7200



# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'USER':'root',
        #'PASSWORD':'M@tech@pp1234',
        # 'PASSWORD':'',
        # 'HOST':'127.0.0.1',
        # 'PORT':'3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/



STATIC_URL = 'static/'

# STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/' 

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('API_KEY'),
    'API_SECRET': env('API_SECRET')
}


EMAIL_BACKEND =  env('EMAIL_BACKEND')
EMAIL_HOST =  env('EMAIL_HOST')
EMAIL_USE_TLS =  env('EMAIL_USE_TLS')
EMAIL_PORT =  env('EMAIL_PORT')
EMAIL_HOST_USER =  env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD =  env('EMAIL_HOST_PASSWORD')


AUTH_USER_MODEL = 'core.User'

LOGIN_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

