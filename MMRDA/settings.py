from pathlib import Path
from datetime import timedelta
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# # use this if setting up on Windows 10 with GDAL installed from OSGeo4W using defaults
if os.name == 'nt':
    VIRTUAL_ENV_BASE = os.environ['VIRTUAL_ENV']
    os.environ['PATH'] = os.path.join(VIRTUAL_ENV_BASE, r'.\Lib\site-packages\osgeo') + ';' + os.environ['PATH']
    os.environ['PROJ_LIB'] = os.path.join(VIRTUAL_ENV_BASE, r'.\Lib\site-packages\osgeo\data\proj') + ';' + os.environ['PATH']


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=idl@@6e_f-wsi#l0%4af02&xht!-7ppi23dt_wo2_6i&fnsca'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'Auth.User'


# Application definition

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'Dashboard',
    'Auth.apps.AuthConfig',
    'EnvMonitoring',
    'SocialMonitoring',
    'Training.apps.TrainingConfig' ,
    'Report',
    "corsheaders",
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django.contrib.gis',
    'rest_framework_gis',
    'django_filters',
    'GIS'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True


ROOT_URLCONF = 'MMRDA.urls'

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

WSGI_APPLICATION = 'MMRDA.wsgi.application'

PASSWORD_RESET_TIMEOUT = 900  # 900 SEC = 15 min
# Email Configuarations 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "Enter your email address"
EMAIL_HOST_PASSWORD = "Enter Your Passwords"
EMAIL_USE_TLS = True

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES={
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME':'MMRDA',
        'USER':'postgres',
        'PASSWORD':'admin',
        'HOST':'10.202.100.7',
        'PORT':'5432',
    }
}


# DATABASES={
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME':'Mdb',
#         'USER':'postgres',
#         'PASSWORD':'password',
#         'HOST':'localhost',
#         'PORT':'5432',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_ROOT = BASE_DIR /"media"
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTHENTICATION_BACKENDS = [
  
#     "django.contrib.auth.backends.ModelBackend",
 
# ]


REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',
        
    ),

    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']

   
}


DATE_FORMAT = '%d-%m-%y'

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "JWT [Bearer {JWT}]": {
            "name": "Authorization",
            "type": "apiKey",
            "in": "header",
        }
    },
    
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300),   # 2 Hours 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
  


    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
}

TIME_ZONE =  'Asia/Kolkata'

GDAL_LIBRARY_PATH = r"C:\OSGeo4W64\bin\gdal301.dll"

